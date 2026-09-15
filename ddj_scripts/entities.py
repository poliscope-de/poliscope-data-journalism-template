from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from setup import poliscope_request

# Entity-IDs (amtliche Regionalschlüssel) haben führende Nullen und müssen als Text gelesen werden.
ENTITY_DTYPES = {"id": str, "postalCode": str}


def load_entities(entities_path: str | Path = "./data/metadata/all_entities.csv") -> pd.DataFrame:
    """Load all Poliscope entities from cache or download them from the API."""
    path = Path(entities_path)

    if path.exists():
        entities_df = pd.read_csv(path, dtype=ENTITY_DTYPES)
        print(f"Entities aus Cache geladen: {len(entities_df)} Einträge ({path})")
        return entities_df

    print("Keine Entity-Liste gefunden - lade alle Entities von der Poliscope API...")
    all_entities: list[dict[str, Any]] = []
    limit = 500
    offset = 0
    total = 1

    while offset < total:
        response = poliscope_request(
            "GET",
            "/entities",
            params={"limit": limit, "offset": offset, "detail": "standard"},
            timeout=10.0,
        )
        data = response.json()
        items = data.get("data", [])
        all_entities.extend(items)
        total = data.get("meta", {}).get("pagination", {}).get("total", len(items))
        offset += limit
        print(f"Downloaded {min(offset, total)} / {total} items")

    entities_df = pd.DataFrame(all_entities)
    path.parent.mkdir(parents=True, exist_ok=True)
    entities_df.to_csv(path, index=False)
    print(f"{len(entities_df)} Entities gespeichert unter {path}")
    return entities_df
