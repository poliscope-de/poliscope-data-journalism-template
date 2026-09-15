from __future__ import annotations

import pandas as pd


def get_unique_meetings(df: pd.DataFrame, groupType: str | None = None) -> pd.DataFrame:
    """Group chunks belonging to the same meeting/proposal.

    Returns one row per ``groupKey`` with the number of chunks (``chunkCount``)
    and the metadata of the first chunk of that group.
    """
    columns = ["groupKey", "groupType", "date", "chunkCount", "proposalId", "entityId", "entityLevel"]
    if df.empty:
        return pd.DataFrame(columns=columns)

    rows = df.copy()
    if "groupType" not in rows.columns:
        rows["groupType"] = rows["groupKey"].astype(str).str.split(":", n=1).str[0]
    if groupType:
        rows = rows[rows["groupType"] == groupType]

    result = (
        rows.groupby("groupKey", sort=False)
        .agg(
            groupType=("groupType", "first"),
            date=("date", "first"),
            chunkCount=("groupKey", "size"),
            proposalId=("proposalId", "first"),
            entityId=("entityId", "first"),
            entityLevel=("entityLevel", "first"),
        )
        .reset_index()
    )
    return result[columns]


def add_entity_name(data: pd.DataFrame, entities: pd.DataFrame) -> pd.DataFrame:
    """Attach the entity name to grouped result rows using the entity ID.

    IDs are compared as strings, because entity IDs like ``03401`` lose their
    leading zeros when a CSV is read back with the default pandas dtypes.
    """
    data = data.copy()
    lookup = entities.drop_duplicates(subset=["id"]).assign(id=lambda e: e["id"].astype(str)).set_index("id")["name"]
    data["entityName"] = data["entityId"].astype(str).map(lookup)
    return data
