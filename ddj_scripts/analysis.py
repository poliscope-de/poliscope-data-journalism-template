from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def load_theme(path: str | Path) -> dict:
    """Load a theme JSON file."""
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def altair_theme(theme_data: dict) -> dict:
    """Build the dict an Altair theme function must return (``{"config": ...}``).

    Only the ``config`` part of the theme file is a valid Vega-Lite config. The
    ``colors`` palette is meant for manual use, e.g. ``theme_data["colors"]["brand"]["500"]``.
    """
    return {"config": theme_data.get("config", {})}


def get_text_color(theme_data: dict) -> str | None:
    """Return the text colour of the theme (axis title colour, else brand colour)."""
    axis_color = theme_data.get("config", {}).get("axis", {}).get("titleColor")
    return axis_color or theme_data.get("colors", {}).get("brand", {}).get("500")


def build_entity_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Build the per-city counts used in the aggregated summaries."""
    return (
        df.assign(city=df["entityName"].fillna("Unknown"))
        .groupby("city")
        .size()
        .reset_index(name="match_count")
    )


def build_histogram(entity_counts: pd.DataFrame, *, bin_size: int = 5) -> pd.DataFrame:
    """Create histogram bins for match counts per entity."""
    bins = np.arange(0, entity_counts["match_count"].max() + bin_size, bin_size)
    hist_counts, bin_edges = np.histogram(entity_counts["match_count"], bins=bins)
    histogram_df = pd.DataFrame({
        "bin_start": bin_edges[:-1],
        "bin_end": bin_edges[1:],
        "count": hist_counts,
    })
    histogram_df["bin_label"] = histogram_df["bin_start"].astype(int).astype(str) + "–" + histogram_df["bin_end"].astype(int).astype(str)
    return histogram_df


def build_weekly_matches(df: pd.DataFrame, *, start_date: str = "2023-07-01") -> pd.DataFrame:
    """Group matches by week for temporal analysis.

    Poliscope only has a near-complete data set from about early 2024 on, so the
    default cut-off hides the sparse older data.
    """
    subset = df.copy()
    subset["date"] = pd.to_datetime(subset["date"], errors="coerce")
    subset = subset.dropna(subset=["date"])
    subset = subset[subset["date"] >= pd.Timestamp(start_date)]
    weekly = (
        subset.assign(week=subset["date"].dt.to_period("W-MON").dt.to_timestamp())
        .groupby("week")
        .size()
        .reset_index(name="matches")
    )
    weekly = weekly.sort_values("week").reset_index(drop=True)
    weekly["week_label"] = weekly["week"].dt.strftime("%Y-%m-%d")
    return weekly
