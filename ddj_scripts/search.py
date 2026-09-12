from __future__ import annotations

from datetime import datetime as dt
from pathlib import Path
from typing import Any

import pandas as pd

from setup import poliscope_request


def fetch_search_results(
    search_terms: list[str],
    *,
    entity_filter: str | None = None,
    thema: str = "search",
    raw_dir: str | Path = "./data/raw",
    datestring: str | None = None,
) -> pd.DataFrame:
    """Search Poliscope for a list of terms and save the raw result set."""
    search_string = " OR ".join(search_terms)
    print(f"🔍 Suche nach: {search_string}")

    all_items: list[dict[str, Any]] = []
    limit = 499
    offset = 0
    total_items: int | None = None
    request_count = 0

    while True:
        request_params = {"q": search_string, "limit": limit, "offset": offset}
        if entity_filter:
            request_params["entityIds"] = [f"{entity_filter}*"]

        response = poliscope_request("GET", "/search/scan", params=request_params, timeout=10.0)
        request_count += 1

        data = response.json()
        items = data.get("data", [])
        pagination = data.get("meta", {}).get("pagination", {})
        total_items = pagination.get("total", 0)

        if not items:
            print("  → Keine weiteren Treffer.")
            break

        all_items.extend(items)
        offset += len(items)
        print(f"  → {offset} / {total_items} Treffer geladen (Request #{request_count})")

        if offset >= total_items or len(items) < limit:
            break

    items_df = pd.DataFrame(all_items)
    print(f"\n✓ FERTIG! {len(items_df)} Treffer insgesamt.")

    if datestring is None:
        datestring = dt.now().strftime("%Y-%m-%d")

    items_path = Path(raw_dir) / f"{datestring}_{thema}_items.csv"
    items_path.parent.mkdir(parents=True, exist_ok=True)
    items_df.to_csv(items_path, index=False)
    print(f"Gespeichert unter {items_path}")
    return items_df
