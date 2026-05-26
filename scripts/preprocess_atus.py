#!/usr/bin/env python3
"""Prepare browser-ready 2024 ATUS data for The Museum of Wasted Time.

The primary path downloads the official BLS 2024 Activity Summary and
Respondent ZIP files, joins respondent age and final weights, maps activity
codes into seven product-facing categories, and writes small CSV outputs.

BLS sometimes blocks automated requests. When the raw files cannot be fetched,
the script writes a deterministic fallback dataset with the same schema so the
static site remains runnable. Re-run with local ZIPs or a successful download to
replace the fallback outputs.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / ".cache" / "atus"

URLS = {
    "summary": "https://www.bls.gov/tus/datafiles/atussum-2024.zip",
    "respondent": "https://www.bls.gov/tus/datafiles/atusresp-2024.zip",
}

CATEGORY_ORDER = [
    "Sleep",
    "Work",
    "Education",
    "Household Activities",
    "Leisure",
    "Caregiving",
    "Travel",
]

FALLBACK = {
    "18-24": {
        "Sleep": {
            "minutes": 548,
            "sub": {
                "Sleeping and sleeplessness": 518,
                "Personal care": 30,
            },
        },
        "Work": {
            "minutes": 192,
            "sub": {
                "Working": 164,
                "Work-related activities": 28,
            },
        },
        "Education": {
            "minutes": 76,
            "sub": {
                "Classes": 42,
                "Homework and research": 28,
                "Education-related activities": 6,
            },
        },
        "Household Activities": {
            "minutes": 118,
            "sub": {
                "Housework and maintenance": 46,
                "Food preparation": 38,
                "Shopping and services": 34,
            },
        },
        "Leisure": {
            "minutes": 375,
            "sub": {
                "TV and video": 128,
                "Socializing": 72,
                "Games and computer use": 58,
                "Sports and exercise": 35,
                "Eating and drinking": 82,
            },
        },
        "Caregiving": {
            "minutes": 39,
            "sub": {
                "Household child care": 20,
                "Adult and nonhousehold care": 14,
                "Care-related services": 5,
            },
        },
        "Travel": {
            "minutes": 92,
            "sub": {
                "Work travel": 27,
                "School travel": 18,
                "Shopping and errand travel": 19,
                "Social and leisure travel": 28,
            },
        },
    },
    "65+": {
        "Sleep": {
            "minutes": 525,
            "sub": {
                "Sleeping and sleeplessness": 496,
                "Personal care": 29,
            },
        },
        "Work": {
            "minutes": 58,
            "sub": {
                "Working": 48,
                "Work-related activities": 10,
            },
        },
        "Education": {
            "minutes": 9,
            "sub": {
                "Classes": 3,
                "Homework and research": 2,
                "Education-related activities": 4,
            },
        },
        "Household Activities": {
            "minutes": 198,
            "sub": {
                "Housework and maintenance": 78,
                "Food preparation": 62,
                "Shopping and services": 58,
            },
        },
        "Leisure": {
            "minutes": 545,
            "sub": {
                "TV and video": 258,
                "Socializing": 62,
                "Reading and relaxing": 82,
                "Sports and exercise": 32,
                "Eating and drinking": 111,
            },
        },
        "Caregiving": {
            "minutes": 35,
            "sub": {
                "Household child care": 8,
                "Adult and nonhousehold care": 20,
                "Care-related services": 7,
            },
        },
        "Travel": {
            "minutes": 70,
            "sub": {
                "Work travel": 7,
                "Shopping and errand travel": 31,
                "Medical and care travel": 12,
                "Social and leisure travel": 20,
            },
        },
    },
}


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 10_000:
        return dest
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 ATUS classroom data preparation",
            "Accept": "application/zip,text/csv,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read()
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise RuntimeError(f"BLS did not return a ZIP for {url}")
    dest.write_bytes(payload)
    return dest


def read_first_table(zip_path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as zf:
        candidates = [
            name
            for name in zf.namelist()
            if name.lower().endswith((".csv", ".dat", ".txt"))
        ]
        if not candidates:
            raise RuntimeError(f"No table found in {zip_path}")
        with zf.open(candidates[0]) as file:
            return pd.read_csv(file)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip().upper() for col in df.columns]
    return df


def find_column(columns: list[str], options: list[str], pattern: str | None = None) -> str | None:
    for option in options:
        if option in columns:
            return option
    if pattern:
        regex = re.compile(pattern)
        for col in columns:
            if regex.fullmatch(col):
                return col
    return None


def code_to_category(code: str) -> tuple[str, str] | None:
    digits = re.sub(r"\D", "", str(code))
    if len(digits) < 2:
        return None
    tier1 = digits[:2]
    tier2 = digits[:4]

    if tier1 == "01":
        return "Sleep", "Sleeping and personal care"
    if tier1 == "05":
        return "Work", "Work and work-related activities"
    if tier1 == "06":
        return "Education", "Education"
    if tier1 in {"02", "07"} or tier2 in {"0801", "0802", "0803", "0804", "0805", "0806", "0807", "0808", "0809"}:
        return "Household Activities", "Household, shopping, and services"
    if tier1 in {"03", "04", "08"}:
        return "Caregiving", "Caregiving"
    if tier1 == "18":
        return "Travel", travel_subcategory(digits)
    if tier1 in {"11", "12", "13"}:
        return "Leisure", "Eating, socializing, and leisure"
    if tier1 in {"10", "14", "15", "16"}:
        return "Leisure", "Civic, religious, and other personal time"
    return "Leisure", "Other daily activities"


def travel_subcategory(code: str) -> str:
    if code.startswith("1805"):
        return "Work travel"
    if code.startswith("1806"):
        return "School travel"
    if code.startswith("1802") or code.startswith("1807") or code.startswith("1808"):
        return "Shopping and errand travel"
    if code.startswith("1803") or code.startswith("1804"):
        return "Care travel"
    return "Social and leisure travel"


def preprocess_from_bls(summary_path: Path | None = None, respondent_path: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_zip = summary_path or download(URLS["summary"], CACHE_DIR / "atussum-2024.zip")
    respondent_zip = respondent_path or download(URLS["respondent"], CACHE_DIR / "atusresp-2024.zip")
    summary = normalize_columns(read_first_table(summary_zip))
    respondent = normalize_columns(read_first_table(respondent_zip))

    id_col = find_column(list(summary.columns), ["TUCASEID", "CASEID"])
    resp_id_col = find_column(list(respondent.columns), ["TUCASEID", "CASEID"])
    age_col = find_column(list(respondent.columns), ["TEAGE", "AGE"])
    weight_col = find_column(list(respondent.columns), ["TUFINLWGT", "TUFNWGTP", "FINALWT"], r".*WGT.*")
    if not id_col or not resp_id_col or not age_col:
        raise RuntimeError("Could not identify respondent id and age columns in ATUS files")

    respondent = respondent[[resp_id_col, age_col] + ([weight_col] if weight_col else [])].rename(
        columns={resp_id_col: "TUCASEID", age_col: "age", weight_col: "weight"} if weight_col else {resp_id_col: "TUCASEID", age_col: "age"}
    )
    if "weight" not in respondent.columns:
        respondent["weight"] = 1.0

    if id_col != "TUCASEID":
        summary = summary.rename(columns={id_col: "TUCASEID"})

    long = reshape_summary(summary)
    merged = long.merge(respondent, on="TUCASEID", how="left")
    merged["age_group"] = pd.cut(
        merged["age"],
        bins=[17, 24, 64, 150],
        labels=["18-24", "drop", "65+"],
        right=True,
    )
    merged = merged[merged["age_group"].isin(["18-24", "65+"])].copy()
    mapped = merged["activity_code"].map(code_to_category)
    merged = merged[mapped.notna()].copy()
    merged[["category", "subcategory"]] = pd.DataFrame(mapped.dropna().tolist(), index=merged.index)

    return aggregate(merged)


def reshape_summary(summary: pd.DataFrame) -> pd.DataFrame:
    code_col = find_column(list(summary.columns), ["TRCODEP", "TRTIER3P", "ACTIVITY_CODE", "ACTIVITY"])
    minutes_col = find_column(list(summary.columns), ["TUACTDUR24", "DURATION", "MINUTES", "ACTIVITY_DURATION"])
    if code_col and minutes_col:
        return summary[["TUCASEID", code_col, minutes_col]].rename(
            columns={code_col: "activity_code", minutes_col: "minutes"}
        )

    wide_cols = [col for col in summary.columns if re.fullmatch(r"T?\d{6}", col)]
    if not wide_cols:
        raise RuntimeError("Could not identify long or wide activity-minute columns")
    long = summary.melt(
        id_vars=["TUCASEID"],
        value_vars=wide_cols,
        var_name="activity_code",
        value_name="minutes",
    )
    long["activity_code"] = long["activity_code"].str.replace(r"^T", "", regex=True)
    return long[long["minutes"].fillna(0) > 0]


def aggregate(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    respondent_counts = df.groupby("age_group")["TUCASEID"].nunique().to_dict()
    grouped = (
        df.groupby(["age_group", "category", "subcategory", "TUCASEID", "weight"], observed=True)["minutes"]
        .sum()
        .reset_index()
    )

    rows = []
    for keys, part in grouped.groupby(["age_group", "category", "subcategory"], observed=True):
        age_group, category, subcategory = keys
        avg_minutes = weighted_mean(part["minutes"], part["weight"])
        rows.append(
            {
                "age_group": age_group,
                "category": category,
                "subcategory": subcategory,
                "avg_minutes_per_day": avg_minutes,
                "avg_hours_per_day": avg_minutes / 60,
                "yearly_hours": avg_minutes / 60 * 365,
                "sample_size": respondent_counts.get(age_group, part["TUCASEID"].nunique()),
            }
        )
    sub = pd.DataFrame(rows)
    main = (
        sub.groupby(["age_group", "category"], observed=True)
        .agg(
            avg_minutes_per_day=("avg_minutes_per_day", "sum"),
            sample_size=("sample_size", "max"),
        )
        .reset_index()
    )
    main["avg_hours_per_day"] = main["avg_minutes_per_day"] / 60
    main["yearly_hours"] = main["avg_hours_per_day"] * 365
    return order_outputs(main, sub)


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    values = pd.to_numeric(values, errors="coerce").fillna(0)
    weights = pd.to_numeric(weights, errors="coerce").fillna(1)
    if weights.sum() == 0:
        return float(values.mean())
    return float((values * weights).sum() / weights.sum())


def fallback_outputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    main_rows = []
    sub_rows = []
    sample_sizes = {"18-24": 800, "65+": 1400}
    for age_group, categories in FALLBACK.items():
        for category, payload in categories.items():
            minutes = payload["minutes"]
            main_rows.append(row(age_group, category, None, minutes, sample_sizes[age_group]))
            for subcategory, sub_minutes in payload["sub"].items():
                sub_rows.append(row(age_group, category, subcategory, sub_minutes, sample_sizes[age_group]))
    return order_outputs(pd.DataFrame(main_rows), pd.DataFrame(sub_rows))


def row(age_group: str, category: str, subcategory: str | None, minutes: float, sample_size: int) -> dict:
    result = {
        "age_group": age_group,
        "category": category,
        "avg_minutes_per_day": round(minutes, 2),
        "avg_hours_per_day": round(minutes / 60, 4),
        "yearly_hours": round(minutes / 60 * 365, 2),
        "sample_size": sample_size,
    }
    if subcategory is not None:
        result["subcategory"] = subcategory
    return result


def order_outputs(main: pd.DataFrame, sub: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    for df in (main, sub):
        df["category"] = pd.Categorical(df["category"], CATEGORY_ORDER, ordered=True)
        df["age_group"] = pd.Categorical(df["age_group"], ["18-24", "65+"], ordered=True)
    main = main.sort_values(["age_group", "category"]).reset_index(drop=True)
    sub = sub.sort_values(["age_group", "category", "subcategory"]).reset_index(drop=True)
    return main, sub


def write_outputs(main: pd.DataFrame, sub: pd.DataFrame, source: str) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    main.to_csv(DATA_DIR / "atus_2024_main_categories.csv", index=False)
    sub.to_csv(DATA_DIR / "atus_2024_subcategories.csv", index=False)
    meta = {
        "source": source,
        "generated_files": [
            "data/atus_2024_main_categories.csv",
            "data/atus_2024_subcategories.csv",
        ],
        "category_totals_minutes": main.groupby("age_group", observed=True)["avg_minutes_per_day"].sum().round(2).to_dict(),
    }
    (DATA_DIR / "atus_2024_metadata.json").write_text(json.dumps(meta, indent=2) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary-zip", type=Path, help="Path to a local ATUS 2024 Activity Summary ZIP.")
    parser.add_argument("--respondent-zip", type=Path, help="Path to a local ATUS 2024 Respondent ZIP.")
    parser.add_argument("--no-fallback", action="store_true", help="Fail instead of writing fallback data when BLS downloads are blocked.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if bool(args.summary_zip) != bool(args.respondent_zip):
            raise RuntimeError("Provide both --summary-zip and --respondent-zip, or neither.")
        main_df, sub_df = preprocess_from_bls(args.summary_zip, args.respondent_zip)
        source = "BLS 2024 ATUS microdata"
    except Exception as exc:
        if args.no_fallback:
            raise
        print(f"Warning: using fallback data because BLS preprocessing failed: {exc}", file=sys.stderr)
        main_df, sub_df = fallback_outputs()
        source = "deterministic fallback shaped like BLS 2024 ATUS output"
    write_outputs(main_df, sub_df, source)
    print("Wrote data/atus_2024_main_categories.csv")
    print("Wrote data/atus_2024_subcategories.csv")
    print("Totals by age group:")
    print(main_df.groupby("age_group", observed=True)["avg_minutes_per_day"].sum())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
