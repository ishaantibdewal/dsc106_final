#!/usr/bin/env python3
"""Generate static SVG checkpoint figures from processed ATUS data."""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".cache" / "matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "figures"

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
LEISURE_GROUPS = [
    "Television and movies",
    "Socializing",
    "Reading",
    "Sports/exercise",
    "Computer/games",
    "Other leisure",
]
COLORS = {
    "Sleep": "#4E79A7",
    "Work": "#F28E2B",
    "Education": "#59A14F",
    "Household Activities": "#B07AA1",
    "Leisure": "#E15759",
    "Caregiving": "#76B7B2",
    "Travel": "#9C755F",
    "Alone": "#4E79A7",
    "Together": "#F28E2B",
    "Not asked": "#BDBDBD",
    "Unknown": "#8CD17D",
}
SOURCE = "Source: 2024 American Time Use Survey, U.S. Bureau of Labor Statistics."
FIGSIZE = (16, 9)
EXPORT_DPI = 300
SAVED_OUTPUTS: list[tuple[Path, Path]] = []
LAYOUT_ADJUSTMENTS = [
    "Saved each chart as SVG and 300 dpi PNG on a fixed 16:9 canvas.",
    "Expanded title/subtitle space by lowering plot tops and using figure-level title text.",
    "Moved crowded legends into reserved bottom or right-side figure bands.",
    "Reduced the daily-rhythm x-axis to 3-hour ticks and removed the x-axis label to keep the legend clear.",
    "Used a shared y-axis scale for the room small multiples so room sizes are comparable.",
]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 14,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 13,
        "svg.fonttype": "none",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def main() -> int:
    FIGURES.mkdir(parents=True, exist_ok=True)
    room = read_csv("age_room_summary.csv")
    sub = read_csv("age_room_subcategories.csv")
    rhythm = read_csv("age_daily_rhythm.csv")
    social = read_csv("age_social_context.csv")

    stacked_24_hour_day_by_age(room)
    room_size_by_age(room)
    biggest_shifts(room)
    leisure_breakdown(sub)
    daily_rhythm_heatmap(rhythm)
    alone_vs_together(social)
    print("\nSaved outputs:")
    for svg_path, png_path in SAVED_OUTPUTS:
        print(f"  {svg_path.relative_to(ROOT)}")
        print(f"  {png_path.relative_to(ROOT)}")
    print("\nLayout adjustments made:")
    for note in LAYOUT_ADJUSTMENTS:
        print(f"  - {note}")
    return 0


def read_csv(filename: str) -> pd.DataFrame:
    path = PROCESSED / filename
    df = pd.read_csv(path)
    print(f"Loaded {path.relative_to(ROOT)}")
    print("Columns:", ", ".join(df.columns))
    return df


def stacked_24_hour_day_by_age(room: pd.DataFrame) -> None:
    table = pivot_room(room, "avg_hours_per_day")
    fig, ax = plt.subplots(figsize=FIGSIZE)
    left = np.zeros(len(table))
    y = np.arange(len(table))
    for room_name in ROOMS:
        values = table[room_name].to_numpy()
        ax.barh(y, values, left=left, color=COLORS[room_name], label=room_name)
        left += values
    ax.set_yticks(y, table.index)
    ax.invert_yaxis()
    ax.set_xlim(0, 24)
    ax.set_xlabel("Weighted average hours per day")
    ax.set_xticks(np.arange(0, 25, 4))
    add_titles(
        fig,
        "A day changes shape with age",
        "The museum rooms show where time moves: school fades, work shrinks later in life, and leisure grows after 55.",
    )
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="center left", bbox_to_anchor=(0.80, 0.49), frameon=False, labelspacing=1.0)
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    add_callout(
        ax,
        "Education is most visible\nin ages 18-24",
        xy=(table.loc["18-24", "Sleep"] + table.loc["18-24", "Work"] + table.loc["18-24", "Education"] / 2, 0),
        xytext=(11.8, -0.62),
    )
    add_callout(
        ax,
        "Leisure expands sharply\nafter 55",
        xy=(table.loc["65+", ["Sleep", "Work", "Education", "Household Activities"]].sum() + table.loc["65+", "Leisure"] / 2, 5),
        xytext=(15.25, 4.2),
    )
    add_callout(
        ax,
        "Sleep is the largest room\nfor every age group",
        xy=(table.loc["35-44", "Sleep"] / 2, 2),
        xytext=(0.9, 4.95),
    )
    clean(ax)
    add_source(fig)
    save(fig, "stacked_24_hour_day_by_age.svg")
    leisure_gain = table.loc["65+", "Leisure"] - table.loc["18-24", "Leisure"]
    work_loss = table.loc["65+", "Work"] - table.loc["18-24", "Work"]
    interpret(
        "stacked_24_hour_day_by_age",
        f"The full-day stack shows the life-cycle tradeoff clearly: ages 65+ spend {leisure_gain:.1f} more hours per day in leisure than ages 18-24, while work is {abs(work_loss):.1f} hours lower. Sleep remains the largest block for every group.",
    )


def room_size_by_age(room: pd.DataFrame) -> None:
    table = pivot_room(room, "avg_hours_per_day")
    fig, axes = plt.subplots(2, 4, figsize=FIGSIZE)
    x = np.arange(len(AGE_GROUPS))
    flat_axes = axes.ravel()
    shared_ymax = np.ceil(table.max().max())
    for ax, room_name in zip(flat_axes, ROOMS):
        values = table.loc[AGE_GROUPS, room_name].to_numpy()
        ax.plot(x, values, color=COLORS[room_name], linewidth=3)
        ax.scatter(x, values, color=COLORS[room_name], s=36, zorder=3)
        ax.fill_between(x, values, color=COLORS[room_name], alpha=0.10)
        ax.set_title(room_name, loc="left", fontsize=15, fontweight="bold", color="#202020", pad=8)
        ax.set_xticks(x, AGE_GROUPS)
        ax.tick_params(axis="x", labelrotation=35)
        ax.set_ylim(0, shared_ymax)
        ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
        clean(ax)
    for ax in flat_axes:
        ax.set_ylabel("")
    axes[0, 0].set_ylabel("Hours/day")
    axes[1, 0].set_ylabel("Hours/day")
    flat_axes[-1].axis("off")
    add_titles(
        fig,
        "Each room follows a different life-course pattern",
        "Small multiples use the same y-axis scale so room sizes are comparable across age groups.",
    )
    add_source(fig)
    save(fig, "room_size_by_age.svg")
    work_peak_age = table["Work"].idxmax()
    leisure_peak_age = table["Leisure"].idxmax()
    interpret(
        "room_size_by_age",
        f"Work reaches its largest average footprint for ages {work_peak_age}, while leisure is highest for ages {leisure_peak_age}. The room metaphor helps show that time is reallocated rather than simply gained or lost.",
    )


def biggest_shifts(room: pd.DataFrame) -> None:
    table_minutes = pivot_room(room, "avg_minutes_per_day")
    diff_minutes = (table_minutes.loc["65+"] - table_minutes.loc["18-24"]).sort_values()
    diff = diff_minutes / 60
    colors = [COLORS[idx] for idx in diff.index]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.barh(diff.index, diff.values, color=colors)
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_xlabel("Hours/day, ages 65+ minus ages 18-24")
    for y_pos, value in enumerate(diff.values):
        minutes = diff_minutes.iloc[y_pos]
        if abs(value) < 0.2:
            continue
        x_text = value + (0.14 if value >= 0 else -0.14)
        ha = "left" if value >= 0 else "right"
        ax.text(x_text, y_pos, f"{value:+.1f} hrs/day", va="center", ha=ha, fontsize=13)
    pad = max(abs(diff.min()), abs(diff.max())) * 1.18
    ax.set_xlim(-pad, pad)
    add_titles(
        fig,
        "The biggest shift is from work to leisure",
        "From young adulthood to 65+, work and education shrink while leisure and household time grow.",
    )
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    clean(ax)
    add_source(fig)
    save(fig, "biggest_shifts_18_24_vs_65_plus.svg")
    biggest_gain = diff.idxmax()
    biggest_loss = diff.idxmin()
    interpret(
        "biggest_shifts_18_24_vs_65_plus",
        f"The largest increase from ages 18-24 to 65+ is {biggest_gain.lower()} ({diff.max():+.1f} hours/day), while the largest decrease is {biggest_loss.lower()} ({diff.min():+.1f} hours/day). Work and education move left of zero; leisure and household activities move right.",
    )


def leisure_breakdown(sub: pd.DataFrame) -> None:
    leisure = sub[sub["room"] == "Leisure"].copy()
    leisure["leisure_group"] = leisure["subcategory"].map(leisure_group)
    table = (
        leisure.pivot_table(
            index="age_group",
            columns="leisure_group",
            values="avg_minutes_per_day",
            aggfunc="sum",
            observed=True,
        )
        .reindex(index=AGE_GROUPS, columns=LEISURE_GROUPS)
        .fillna(0)
        / 60
    )
    fig, ax = plt.subplots(figsize=FIGSIZE)
    bottom = np.zeros(len(table))
    y = np.arange(len(table))
    palette = leisure_palette(len(LEISURE_GROUPS))
    for color, name in zip(palette, LEISURE_GROUPS):
        values = table[name].to_numpy()
        ax.barh(y, values, left=bottom, color=color, label=name)
        bottom += values
    ax.set_yticks(y, table.index)
    ax.invert_yaxis()
    ax.set_xlabel("Weighted average hours/day in leisure")
    ax.set_xlim(0, max(bottom) * 1.08)
    add_titles(
        fig,
        "Older adults spend more leisure time, especially TV/movies",
        "Top leisure groups plus other leisure, shown as hours/day within the leisure room.",
    )
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, ncol=3, loc="lower center", bbox_to_anchor=(0.52, 0.14), frameon=False, columnspacing=1.5)
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    clean(ax)
    add_source(fig)
    save(fig, "leisure_subcategory_breakdown.svg")
    tv_gain = table.loc["65+", "Television and movies"] - table.loc["18-24", "Television and movies"]
    interpret(
        "leisure_subcategory_breakdown",
        f"Leisure time increases with age, and television/movies account for about {tv_gain:.1f} additional hours/day from ages 18-24 to 65+. Grouping the long tail into 'Other leisure' makes the proposal takeaway much clearer.",
    )


def daily_rhythm_heatmap(rhythm: pd.DataFrame) -> None:
    dominant = (
        rhythm.sort_values("avg_minutes_per_day")
        .groupby(["age_group", "hour"], observed=True)
        .tail(1)
        .copy()
    )
    room_to_int = {room: idx for idx, room in enumerate(ROOMS)}
    matrix = dominant.pivot(index="age_group", columns="hour", values="room").reindex(AGE_GROUPS)
    encoded = matrix.map(room_to_int.get).to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    cmap = plt.matplotlib.colors.ListedColormap([COLORS[room] for room in ROOMS])
    ax.imshow(encoded, aspect="auto", cmap=cmap, vmin=-0.5, vmax=len(ROOMS) - 0.5)
    tick_hours = [0, 3, 6, 9, 12, 15, 18, 21]
    ax.set_xticks(tick_hours, hour_labels(tick_hours))
    ax.set_yticks(range(len(AGE_GROUPS)), AGE_GROUPS)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelrotation=0)
    ax.set_xticks(np.arange(-0.5, 24, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(AGE_GROUPS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.4)
    ax.tick_params(which="minor", bottom=False, left=False)
    add_titles(
        fig,
        "Which room dominates each hour of the day?",
        "Each cell shows the room with the highest weighted average minutes during that clock hour for each age group.",
    )
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[room]) for room in ROOMS]
    fig.legend(
        handles,
        ROOMS,
        ncol=4,
        loc="lower center",
        bbox_to_anchor=(0.53, 0.13),
        frameon=False,
        columnspacing=1.8,
        handlelength=1.2,
        handletextpad=0.5,
    )
    add_callout(
        ax,
        "35-44 shifts into leisure\nafter the workday",
        xy=(20, AGE_GROUPS.index("35-44")),
        xytext=(17.2, -1.12),
    )
    clean(ax)
    add_source(fig)
    save(fig, "daily_rhythm_heatmap.svg")
    interpret(
        "daily_rhythm_heatmap",
        "The heatmap turns the dataset into a schedule: sleep dominates overnight, work and household/care activities take over during daytime hours, and leisure expands in the evening. This supports using the website as a time-based museum walkthrough.",
    )


def alone_vs_together(social: pd.DataFrame) -> None:
    minutes = (
        social.pivot_table(
            index="age_group",
            columns="social_context",
            values="avg_minutes_per_day",
            aggfunc="sum",
            observed=True,
        )
        .reindex(AGE_GROUPS)
        .fillna(0)
    )
    if "Together" in minutes.columns:
        minutes = minutes.rename(columns={"Together": "With others"})
    contexts = [name for name in ["Alone", "With others", "Unknown"] if name in minutes.columns and minutes[name].sum() > 0]
    eligible = minutes[contexts].sum(axis=1)
    shares = minutes[contexts].div(eligible, axis=0) * 100

    fig, ax = plt.subplots(figsize=FIGSIZE)
    y = np.arange(len(shares))
    bottom = np.zeros(len(shares))
    context_colors = {
        "Alone": COLORS["Alone"],
        "With others": COLORS["Together"],
        "Unknown": COLORS["Unknown"],
    }
    for name in contexts:
        values = shares[name].to_numpy()
        ax.barh(y, values, left=bottom, color=context_colors[name], label=name)
        bottom += values
    ax.set_yticks(y, shares.index)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of who-context-eligible activity time")
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{value:.0f}%"))
    add_titles(
        fig,
        "How much social-context time is spent alone?",
        "Excluding activities where ATUS did not ask who was present reveals a clearer alone-versus-with-others pattern.",
    )
    for i, age_group in enumerate(shares.index):
        alone = shares.loc[age_group, "Alone"] if "Alone" in shares else 0
        ax.text(alone / 2, i, f"{alone:.0f}%", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, ncol=len(contexts), loc="lower center", bbox_to_anchor=(0.53, 0.15), frameon=False)
    ax.grid(axis="x", color="#E6E6E6", linewidth=0.8)
    add_footnote(fig, "Excludes activities where ATUS did not collect who was present.")
    clean(ax)
    add_source(fig)
    save(fig, "alone_vs_together.svg")
    alone_change = shares.loc["65+", "Alone"] - shares.loc["18-24", "Alone"]
    interpret(
        "alone_vs_together",
        f"After excluding activities where ATUS did not ask who was present, the alone share is {alone_change:+.1f} percentage points higher for ages 65+ than ages 18-24. This version surfaces the social pattern instead of letting the survey artifact dominate the chart.",
    )


def pivot_room(room: pd.DataFrame, value: str) -> pd.DataFrame:
    return (
        room.pivot_table(index="age_group", columns="room", values=value, aggfunc="sum", observed=True)
        .reindex(index=AGE_GROUPS, columns=ROOMS)
        .fillna(0)
    )


def clean(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.tick_params(colors="#333333")
    ax.xaxis.label.set_color("#333333")
    ax.yaxis.label.set_color("#333333")


def add_titles(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(0.055, 0.965, title, ha="left", va="top", fontsize=30, fontweight="bold", color="#202020")
    fig.text(0.055, 0.885, subtitle, ha="left", va="top", fontsize=16, color="#4A4A4A")


def add_source(fig: plt.Figure) -> None:
    fig.text(0.055, 0.032, SOURCE, ha="left", va="bottom", fontsize=10.5, color="#666666")


def add_footnote(fig: plt.Figure, note: str) -> None:
    fig.text(0.055, 0.067, note, ha="left", va="bottom", fontsize=10.5, color="#666666")


def add_callout(ax: plt.Axes, text: str, xy: tuple[float, float], xytext: tuple[float, float]) -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        ha="left",
        va="center",
        fontsize=13,
        color="#202020",
        arrowprops={
            "arrowstyle": "-",
            "color": "#555555",
            "linewidth": 1.1,
            "shrinkA": 0,
            "shrinkB": 3,
        },
        bbox={
            "boxstyle": "round,pad=0.28",
            "facecolor": "white",
            "edgecolor": "#D0D0D0",
            "linewidth": 0.8,
            "alpha": 0.96,
        },
        annotation_clip=False,
    )


def wrap_label(label: str, width: int) -> str:
    return "\n".join(textwrap.wrap(str(label), width=width, break_long_words=False))


def hour_labels(hours: list[int] | None = None) -> list[str]:
    hours = list(range(24)) if hours is None else hours
    labels = []
    for hour in hours:
        if hour == 0:
            labels.append("12 AM")
        elif hour < 12:
            labels.append(f"{hour} AM")
        elif hour == 12:
            labels.append("12 PM")
        else:
            labels.append(f"{hour - 12} PM")
    return labels


def leisure_palette(count: int) -> list[tuple[float, float, float, float]]:
    cmap = LinearSegmentedColormap.from_list("leisure_scale", ["#F7C6C7", COLORS["Leisure"], "#8F2D38"])
    return [cmap(i) for i in np.linspace(0.12, 0.92, count)]


def leisure_group(subcategory: str) -> str:
    label = str(subcategory).lower()
    if "television" in label or "movie" in label:
        return "Television and movies"
    if "socializing" in label or "communicating" in label:
        return "Socializing"
    if "reading" in label:
        return "Reading"
    if "sport" in label or "exercise" in label or "recreation" in label:
        return "Sports/exercise"
    if "computer" in label or "game" in label:
        return "Computer/games"
    return "Other leisure"


def interpret(chart: str, text: str) -> None:
    print(f"Interpretation - {chart}: {text}")


def save(fig: plt.Figure, filename: str) -> None:
    if filename == "leisure_subcategory_breakdown.svg":
        fig.subplots_adjust(left=0.12, right=0.94, top=0.66, bottom=0.34)
    elif filename == "biggest_shifts_18_24_vs_65_plus.svg":
        fig.subplots_adjust(left=0.22, right=0.91, top=0.66, bottom=0.19)
    elif filename == "daily_rhythm_heatmap.svg":
        fig.subplots_adjust(left=0.10, right=0.94, top=0.69, bottom=0.31)
    elif filename == "room_size_by_age.svg":
        fig.subplots_adjust(left=0.07, right=0.97, top=0.66, bottom=0.16, hspace=0.82, wspace=0.40)
    elif filename == "alone_vs_together.svg":
        fig.subplots_adjust(left=0.12, right=0.94, top=0.66, bottom=0.34)
    elif filename == "stacked_24_hour_day_by_age.svg":
        fig.subplots_adjust(left=0.10, right=0.75, top=0.66, bottom=0.20)
    else:
        fig.subplots_adjust(left=0.11, right=0.94, top=0.66, bottom=0.30)
    svg_path = FIGURES / filename
    png_path = svg_path.with_suffix(".png")
    fig.savefig(svg_path, format="svg", facecolor="white")
    fig.savefig(png_path, format="png", dpi=EXPORT_DPI, facecolor="white")
    plt.close(fig)
    SAVED_OUTPUTS.append((svg_path, png_path))
    print(f"Wrote {svg_path.relative_to(ROOT)}")
    print(f"Wrote {png_path.relative_to(ROOT)}")


if __name__ == "__main__":
    raise SystemExit(main())
