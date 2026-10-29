#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Unit tests for the deterministic (non-network) parts of chess_com_fetch.py."""

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import chess_com_fetch as cf  # noqa: E402


class TestMonthRange(unittest.TestCase):
    def test_single_month(self):
        self.assertEqual(list(cf.month_range(date(2026, 5, 1), date(2026, 5, 21))), [(2026, 5)])

    def test_spans_year_boundary(self):
        self.assertEqual(
            list(cf.month_range(date(2026, 12, 15), date(2027, 1, 10))),
            [(2026, 12), (2027, 1)],
        )

    def test_multi_month_same_year(self):
        self.assertEqual(
            list(cf.month_range(date(2026, 3, 1), date(2026, 5, 31))),
            [(2026, 3), (2026, 4), (2026, 5)],
        )


class TestToEntry(unittest.TestCase):
    def test_shapes_expected_fields(self):
        game = {
            "end_time": 1716300000,
            "url": "https://chess.com/game/live/123",
            "time_class": "rapid",
            "time_control": "1800",
            "white": {"username": "alice", "result": "win"},
            "black": {"username": "bob", "result": "checkmated"},
            "pgn": "1. e4 e5",
        }
        entry = cf.to_entry(game)
        self.assertEqual(entry["white"]["username"], "alice")
        self.assertEqual(entry["black"]["result"], "checkmated")
        self.assertEqual(entry["pgn"], "1. e4 e5")
        self.assertTrue(entry["end_time"].startswith("2024-"))


if __name__ == "__main__":
    unittest.main()
