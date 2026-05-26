#!/usr/bin/env python3
"""Preprocess local official 2024 ATUS files for the museum prototype."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

RAW_FILES = {
    "activity": RAW / "atusact-2024" / "atusact_2024.dat",
    "respondent": RAW / "atusresp-2024" / "atusresp_2024.dat",
    "summary": RAW / "atussum-2024" / "atussum_2024.dat",
    "who": RAW / "atuswho-2024" / "atuswho_2024.dat",
    "roster": RAW / "atusrost-2024" / "atusrost_2024.dat",
    "eldercare_roster": RAW / "atusrostec-2024" / "atusrostec_2024.dat",
}
LEXICON = RAW / "lexiconwex2024.xls"

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
ROOMS = [
    "Sleep",
    "Work",
    "Education",
    "Household Activities",
    "Leisure",
    "Caregiving",
    "Travel",
]


def main() -> int:
    PROCESSED.mkdir(parents=True, exist_ok=True)

    data = {name: load_dat(path, name) for name, path in RAW_FILES.items()}
    respondent = add_age_groups(data["respondent"], data["summary"])
    weights = respondent[["TUCASEID", "TEAGE", "age_group", "TUFINLWGT"]].copy()

    lexicon = load_lexicon(LEXICON)
    denominators = age_denominators(weights)
    summary_long = reshape_summary(data["summary"], lexicon)
    summary = summary_long.merge(weights, on="TUCASEID", how="inner", validate="many_to_one")
    summary["room"] = summary["activity_code"].map(map_room)

    age_room_subcategories = aggregate_weighted(
        summary,
        ["age_group", "room", "activity_code", "activity"],
        "minutes",
        denominators,
    ).rename(columns={"activity": "subcategory"})
    age_room_subcategories = order_age_room(age_room_subcategories)

    age_room_summary = (
        age_room_subcategories.groupby(["age_group", "room"], observed=True, as_index=False)
        .agg(
            avg_minutes_per_day=("avg_minutes_per_day", "sum"),
            weighted_respondents=("weighted_respondents", "max"),
            unweighted_respondents=("unweighted_respondents", "max"),
        )
    )
    age_room_summary["avg_hours_per_day"] = age_room_summary["avg_minutes_per_day"] / 60
    age_room_summary = order_age_room(age_room_summary)

    validate_daily_totals(age_room_summary)

    activity = prepare_activity(data["activity"], lexicon).merge(
        weights, on="TUCASEID", how="inner", validate="many_to_one"
    )
    age_daily_rhythm = build_daily_rhythm(activity)

    age_social_context = build_social_context(activity, data["who"])
    life_receipt = build_life_receipt(age_room_summary)

    write_csv(age_room_summary, "age_room_summary.csv")
    write_csv(age_room_subcategories, "age_room_subcategories.csv")
    write_csv(age_daily_rhythm, "age_daily_rhythm.csv")
    write_csv(age_social_context, "age_social_context.csv")
    write_csv(life_receipt, "life_receipt.csv")
    write_metadata(data, lexicon, age_room_summary)
    write_previews(
        {
            "age_room_summary": age_room_summary,
            "age_room_subcategories": age_room_subcategories,
            "age_daily_rhythm": age_daily_rhythm,
            "age_social_context": age_social_context,
            "life_receipt": life_receipt,
        }
    )
    return 0


def load_dat(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", errors="replace") as file:
        first_line = file.readline()
    if "," not in first_line:
        raise ValueError(f"{path} does not appear to be comma-separated.")
    df = pd.read_csv(path)
    df.columns = [str(col).strip().upper() for col in df.columns]
    print(f"\nLoaded {label}: {path}")
    print(f"Rows: {len(df):,}, columns: {len(df.columns):,}")
    print("Columns:", ", ".join(df.columns))
    return df


def add_age_groups(respondent: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    required = {"TUCASEID", "TUFINLWGT"}
    missing = required - set(respondent.columns)
    if missing:
        raise ValueError(f"Respondent file missing required columns: {sorted(missing)}")
    if "TEAGE" in respondent.columns:
        respondent = respondent[["TUCASEID", "TUFINLWGT", "TEAGE"]].copy()
        age_source = "respondent"
    else:
        respondent = respondent[["TUCASEID", "TUFINLWGT"]].copy()
        if "TEAGE" not in summary.columns:
            raise ValueError("Neither respondent nor summary file contains TEAGE.")
        respondent = respondent.merge(summary[["TUCASEID", "TEAGE"]], on="TUCASEID", how="left", validate="one_to_one")
        age_source = "summary"
        print("\nWarning: respondent file does not include TEAGE; using TEAGE from Activity Summary.")
    respondent = respondent.copy()
    respondent.attrs["age_source"] = age_source
    respondent["age_group"] = pd.cut(
        respondent["TEAGE"],
        bins=[17, 24, 34, 44, 54, 64, np.inf],
        labels=AGE_GROUPS,
        right=True,
    )
    respondent = respondent[respondent["age_group"].notna()].copy()
    respondent["age_group"] = respondent["age_group"].astype(str)
    respondent["TUFINLWGT"] = pd.to_numeric(respondent["TUFINLWGT"], errors="coerce")
    return respondent


def load_lexicon(path: Path) -> pd.DataFrame:
    lexicon = pd.read_excel(path, sheet_name="ATUS 2024 Lexicon", header=1)
    lexicon = lexicon.rename(
        columns={
            "6-digit activity code": "activity_code",
            "Activity": "activity",
        }
    )
    lexicon = lexicon[["activity_code", "activity"]].dropna(subset=["activity_code", "activity"])
    lexicon["activity_code"] = lexicon["activity_code"].map(format_code)
    lexicon["activity"] = lexicon["activity"].astype(str).str.strip()
    lexicon = lexicon.drop_duplicates("activity_code").sort_values("activity_code").reset_index(drop=True)
    print(f"\nLoaded lexicon: {path}")
    print(f"Rows: {len(lexicon):,}, columns: {len(lexicon.columns):,}")
    print("Columns:", ", ".join(lexicon.columns))
    return lexicon


def reshape_summary(summary: pd.DataFrame, lexicon: pd.DataFrame) -> pd.DataFrame:
    activity_cols = [col for col in summary.columns if col.startswith("T") and col[1:].isdigit() and len(col) == 7]
    if not activity_cols:
        raise ValueError("Activity Summary file has no t###### minute columns.")
    long = summary.melt(
        id_vars=["TUCASEID"],
        value_vars=activity_cols,
        var_name="activity_code",
        value_name="minutes",
    )
    long["activity_code"] = long["activity_code"].str[1:].map(format_code)
    long["minutes"] = pd.to_numeric(long["minutes"], errors="coerce").fillna(0)
    long = long[long["minutes"] > 0].copy()
    long = long.merge(lexicon, on="activity_code", how="left")
    long["activity"] = long["activity"].fillna("Unmapped activity " + long["activity_code"])
    return long


def prepare_activity(activity: pd.DataFrame, lexicon: pd.DataFrame) -> pd.DataFrame:
    required = {"TUCASEID", "TUACTIVITY_N", "TRCODE", "TUSTARTTIM", "TUSTOPTIME", "TUACTDUR24"}
    missing = required - set(activity.columns)
    if missing:
        raise ValueError(f"Activity file missing required columns: {sorted(missing)}")
    result = activity[list(required)].copy()
    result["activity_code"] = result["TRCODE"].map(format_code)
    result["room"] = result["activity_code"].map(map_room)
    result["duration"] = pd.to_numeric(result["TUACTDUR24"], errors="coerce").fillna(0)
    result = result.merge(lexicon, on="activity_code", how="left")
    result["activity"] = result["activity"].fillna("Unmapped activity " + result["activity_code"])
    return result


def age_denominators(weights: pd.DataFrame) -> dict[str, dict[str, float]]:
    deduped = weights[["TUCASEID", "age_group", "TUFINLWGT"]].drop_duplicates("TUCASEID")
    grouped = deduped.groupby("age_group", observed=True)
    return {
        str(age_group): {
            "weighted_respondents": float(part["TUFINLWGT"].sum()),
            "unweighted_respondents": int(part["TUCASEID"].nunique()),
        }
        for age_group, part in grouped
    }


def aggregate_weighted(
    df: pd.DataFrame,
    group_cols: list[str],
    value_col: str,
    denominators: dict[str, dict[str, float]],
) -> pd.DataFrame:
    case_group = (
        df.groupby(["TUCASEID", "TUFINLWGT", *group_cols], observed=True, as_index=False)[value_col]
        .sum()
        .rename(columns={value_col: "case_minutes"})
    )
    rows = []
    for keys, part in case_group.groupby(group_cols, observed=True, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_cols, keys))
        age_group = str(row.get("age_group"))
        denominator = denominators.get(age_group, {})
        weight_sum = denominator.get("weighted_respondents", float(part["TUFINLWGT"].sum()))
        unweighted = denominator.get("unweighted_respondents", int(part["TUCASEID"].nunique()))
        weights = part["TUFINLWGT"]
        minutes = part["case_minutes"]
        avg = float((minutes * weights).sum() / weight_sum) if weight_sum else float(minutes.mean())
        row.update(
            {
                "avg_minutes_per_day": avg,
                "avg_hours_per_day": avg / 60,
                "weighted_respondents": weight_sum,
                "unweighted_respondents": unweighted,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def build_daily_rhythm(activity: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    for row in activity.itertuples(index=False):
        start = clock_minutes(row.TUSTARTTIM)
        remaining = float(row.duration)
        cursor = start
        while remaining > 0:
            hour = int((cursor // 60) % 24)
            next_hour = ((cursor // 60) + 1) * 60
            chunk = min(remaining, next_hour - cursor)
            pieces.append(
                {
                    "TUCASEID": row.TUCASEID,
                    "age_group": row.age_group,
                    "TUFINLWGT": row.TUFINLWGT,
                    "hour": hour,
                    "room": row.room,
                    "minutes": chunk,
                }
            )
            remaining -= chunk
            cursor += chunk
    hourly = pd.DataFrame(pieces)
    denominators = age_denominators(activity[["TUCASEID", "age_group", "TUFINLWGT"]].drop_duplicates())
    result = aggregate_weighted(hourly, ["age_group", "hour", "room"], "minutes", denominators)
    totals = result.groupby(["age_group", "hour"], observed=True)["avg_minutes_per_day"].transform("sum")
    result["share_of_hour"] = np.where(totals > 0, result["avg_minutes_per_day"] / totals, 0)
    result = order_age_room(result).sort_values(["age_group", "hour", "room"]).reset_index(drop=True)
    return result


def build_social_context(activity: pd.DataFrame, who: pd.DataFrame) -> pd.DataFrame:
    who = who.copy()
    who["is_alone_code"] = who["TUWHO_CODE"].isin([18, 19])
    who_status = (
        who.groupby(["TUCASEID", "TUACTIVITY_N"], as_index=False)
        .agg(
            any_asked=("TRWHONA", lambda s: bool((s == 0).any())),
            any_together=("TUWHO_CODE", lambda s: bool((~s.isin([18, 19, -1, -2, -3])).any())),
            any_alone=("is_alone_code", "any"),
        )
    )
    who_status["social_context"] = np.select(
        [~who_status["any_asked"], who_status["any_together"], who_status["any_alone"]],
        ["Not asked", "Together", "Alone"],
        default="Unknown",
    )
    merged = activity.merge(
        who_status[["TUCASEID", "TUACTIVITY_N", "social_context"]],
        on=["TUCASEID", "TUACTIVITY_N"],
        how="left",
    )
    merged["social_context"] = merged["social_context"].fillna("Not asked")
    denominators = age_denominators(activity[["TUCASEID", "age_group", "TUFINLWGT"]].drop_duplicates())
    result = aggregate_weighted(merged, ["age_group", "social_context"], "duration", denominators)
    totals = result.groupby("age_group", observed=True)["avg_minutes_per_day"].transform("sum")
    result["share_of_day"] = np.where(totals > 0, result["avg_minutes_per_day"] / totals, 0)
    order = {"Alone": 0, "Together": 1, "Not asked": 2, "Unknown": 3}
    result["context_order"] = result["social_context"].map(order).fillna(9)
    result = result.sort_values(["age_group", "context_order"]).drop(columns="context_order").reset_index(drop=True)
    return result


def build_life_receipt(age_room_summary: pd.DataFrame) -> pd.DataFrame:
    receipt = age_room_summary.copy()
    receipt["yearly_hours"] = receipt["avg_hours_per_day"] * 365
    receipt["lifetime_years_80yr"] = receipt["avg_minutes_per_day"] * 365 * 80 / 60 / 24 / 365
    return receipt[
        [
            "age_group",
            "room",
            "avg_minutes_per_day",
            "avg_hours_per_day",
            "yearly_hours",
            "lifetime_years_80yr",
        ]
    ]


def validate_daily_totals(age_room_summary: pd.DataFrame) -> None:
    totals = age_room_summary.groupby("age_group", observed=True)["avg_minutes_per_day"].sum()
    print("\nWeighted daily totals by age group:")
    for age_group, total in totals.items():
        print(f"  {age_group}: {total:.2f} minutes")
    bad = totals[(totals - 1440).abs() > 1.0]
    if not bad.empty:
        raise ValueError(f"Weighted daily totals are not close to 1440 minutes: {bad.to_dict()}")


def write_csv(df: pd.DataFrame, filename: str) -> None:
    path = PROCESSED / filename
    df.to_csv(path, index=False)
    print(f"Wrote {path.relative_to(ROOT)} ({len(df):,} rows)")


def write_previews(outputs: dict[str, pd.DataFrame]) -> None:
    preview = []
    for name, df in outputs.items():
        sample = df.head(10).copy()
        sample.insert(0, "source_table", name)
        preview.append(sample)
    combined = pd.concat(preview, ignore_index=True, sort=False)
    path = PROCESSED / "preview_debug.csv"
    combined.to_csv(path, index=False)
    print(f"Wrote {path.relative_to(ROOT)}")


def write_metadata(data: dict[str, pd.DataFrame], lexicon: pd.DataFrame, age_room_summary: pd.DataFrame) -> None:
    meta = {
        "source": "Official local 2024 ATUS files in data/raw/",
        "generated_at": pd.Timestamp.now(tz="America/Los_Angeles").isoformat(),
        "join_key": "TUCASEID",
        "weight_column": "TUFINLWGT",
        "age_groups": AGE_GROUPS,
        "rooms": ROOMS,
        "raw_rows": {name: int(len(df)) for name, df in data.items()},
        "lexicon_rows": int(len(lexicon)),
        "daily_total_validation_minutes": (
            age_room_summary.groupby("age_group", observed=True)["avg_minutes_per_day"].sum().round(4).to_dict()
        ),
        "outputs": [
            "data/processed/age_room_summary.csv",
            "data/processed/age_room_subcategories.csv",
            "data/processed/age_daily_rhythm.csv",
            "data/processed/age_social_context.csv",
            "data/processed/life_receipt.csv",
            "data/processed/atus_2024_metadata.json",
        ],
    }
    path = PROCESSED / "atus_2024_metadata.json"
    path.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Wrote {path.relative_to(ROOT)}")


def order_age_room(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    if "age_group" in result.columns:
        result["age_group"] = pd.Categorical(result["age_group"], AGE_GROUPS, ordered=True)
    if "room" in result.columns:
        result["room"] = pd.Categorical(result["room"], ROOMS, ordered=True)
    return result.sort_values([col for col in ["age_group", "room"] if col in result.columns]).reset_index(drop=True)


def map_room(activity_code: str) -> str:
    code = format_code(activity_code)
    tier1 = code[:2]
    tier2 = code[:4]
    if tier1 == "01":
        return "Sleep"
    if tier1 == "05":
        return "Work"
    if tier1 == "06":
        return "Education"
    if tier1 in {"02", "07"}:
        return "Household Activities"
    if tier1 in {"03", "04"} or tier2 in {"0801", "0802", "0803", "0804", "0805", "0806", "0807"}:
        return "Caregiving"
    if tier1 == "18":
        return "Travel"
    return "Leisure"


def format_code(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits.zfill(6)[-6:]


def clock_minutes(value: object) -> int:
    text = str(value)
    hour, minute, *_ = [int(part) for part in text.split(":")]
    return hour * 60 + minute


if __name__ == "__main__":
    raise SystemExit(main())
