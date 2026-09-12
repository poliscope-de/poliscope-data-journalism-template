from __future__ import annotations

import pandas as pd


def get_unique_meetings(df: pd.DataFrame, groupType: str | None = None) -> pd.DataFrame:
    """Group chunks belonging to the same meeting/proposal."""
    result = pd.DataFrame(columns=["groupKey", "date", "chunkCount", "proposalId", "entityId", "entityLevel"])

    rows = df[df["groupType"] == groupType] if groupType else df
    unique_group_keys = rows["groupKey"].drop_duplicates()

    for group_key in unique_group_keys:
        chunk_count = len(df[df["groupKey"] == group_key])
        first_instance = df[df["groupKey"] == group_key].iloc[0]

        result.loc[len(result)] = {
            "groupKey": group_key,
            "date": first_instance["date"],
            "chunkCount": chunk_count,
            "proposalId": first_instance["proposalId"],
            "entityId": first_instance["entityId"],
            "entityLevel": first_instance["entityLevel"],
        }

    return result


def add_entity_name(data: pd.DataFrame, entities: pd.DataFrame) -> pd.DataFrame:
    """Attach the entity name to grouped result rows using the entity ID."""
    data = data.copy()
    data["entityName"] = data["entityId"].map(entities.drop_duplicates(subset=["id"]).set_index("id")["name"])
    return data
