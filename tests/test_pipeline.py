import io
import unittest

import pandas as pd

from ddj_scripts.analysis import altair_theme, build_entity_counts, build_histogram, build_weekly_matches, get_text_color
from ddj_scripts.grouping import add_entity_name, get_unique_meetings
from ddj_scripts.search import ITEM_DTYPES


def sample_items() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"groupKey": "meeting:a", "groupType": "meeting", "date": "2024-02-06T17:00:00", "proposalId": None, "entityId": "03401", "entityLevel": "40"},
            {"groupKey": "meeting:a", "groupType": "meeting", "date": "2024-02-06T17:00:00", "proposalId": None, "entityId": "03401", "entityLevel": "40"},
            {"groupKey": "proposal:b", "groupType": "proposal", "date": "2024-02-13T17:00:00", "proposalId": "b", "entityId": "034010000", "entityLevel": "50"},
            {"groupKey": "meeting:c", "groupType": "meeting", "date": "2022-01-01T10:00:00", "proposalId": None, "entityId": "99999", "entityLevel": "60"},
        ]
    )


def sample_entities() -> pd.DataFrame:
    return pd.DataFrame([{"id": "03401", "name": "Delmenhorst, Stadt"}, {"id": "034010000", "name": "Delmenhorst, Stadt"}, {"id": "03pr25", "name": "Kreisfreie Stadt Delmenhorst"}])


class GroupingTests(unittest.TestCase):
    def test_groups_chunks_per_group_key(self):
        grouped = get_unique_meetings(sample_items())

        self.assertEqual(len(grouped), 3)
        self.assertEqual(grouped.set_index("groupKey").loc["meeting:a", "chunkCount"], 2)
        self.assertEqual(list(grouped["groupType"]), ["meeting", "proposal", "meeting"])

    def test_filters_by_group_type(self):
        grouped = get_unique_meetings(sample_items(), groupType="proposal")

        self.assertEqual(list(grouped["groupKey"]), ["proposal:b"])

    def test_derives_group_type_when_missing(self):
        grouped = get_unique_meetings(sample_items().drop(columns=["groupType"]))

        self.assertEqual(list(grouped["groupType"]), ["meeting", "proposal", "meeting"])

    def test_empty_input(self):
        grouped = get_unique_meetings(sample_items().iloc[0:0])

        self.assertTrue(grouped.empty)
        self.assertIn("chunkCount", grouped.columns)

    def test_entity_name_join_survives_csv_roundtrip(self):
        items = sample_items()
        csv_default = pd.read_csv(io.StringIO(items.to_csv(index=False)))  # entityId wird zu int, führende Null weg
        grouped = add_entity_name(get_unique_meetings(csv_default), sample_entities())
        self.assertTrue(grouped["entityName"].iloc[0] != grouped["entityName"].iloc[0])  # NaN: Join schlägt fehl

        csv_typed = pd.read_csv(io.StringIO(items.to_csv(index=False)), dtype=ITEM_DTYPES)
        grouped = add_entity_name(get_unique_meetings(csv_typed), sample_entities())
        self.assertEqual(list(grouped["entityName"].iloc[:2]), ["Delmenhorst, Stadt", "Delmenhorst, Stadt"])
        self.assertTrue(pd.isna(grouped["entityName"].iloc[2]))


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.grouped = add_entity_name(get_unique_meetings(sample_items()), sample_entities())

    def test_entity_counts_and_histogram(self):
        counts = build_entity_counts(self.grouped)
        self.assertEqual(counts.set_index("city").loc["Delmenhorst, Stadt", "match_count"], 2)
        self.assertEqual(counts.set_index("city").loc["Unknown", "match_count"], 1)

        hist = build_histogram(counts, bin_size=5)
        self.assertEqual(hist["count"].sum(), 2)
        self.assertEqual(hist["bin_label"].iloc[0], "0–5")

    def test_weekly_matches_respects_start_date(self):
        weekly = build_weekly_matches(self.grouped, start_date="2023-07-01")
        self.assertEqual(weekly["matches"].sum(), 2)
        self.assertEqual(list(weekly["week_label"]), ["2024-02-06", "2024-02-13"])

    def test_theme_helpers(self):
        theme = {"config": {"axis": {"titleColor": "#123456"}}, "colors": {"brand": {"500": "#abcdef"}}}
        self.assertEqual(altair_theme(theme), {"config": {"axis": {"titleColor": "#123456"}}})
        self.assertEqual(get_text_color(theme), "#123456")
        self.assertEqual(get_text_color({"colors": {"brand": {"500": "#abcdef"}}}), "#abcdef")


if __name__ == "__main__":
    unittest.main()
