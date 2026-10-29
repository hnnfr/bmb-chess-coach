#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["chess>=1.10"]
# ///
"""Unit tests for opening_frequency.py's deterministic tallying."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import opening_frequency as of  # noqa: E402

RUY_LOPEZ = "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6"
ITALIAN = "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5"


class TestOpeningKey(unittest.TestCase):
    def test_caps_at_requested_plies(self):
        key = of.opening_key(RUY_LOPEZ, plies=4)
        self.assertEqual(key, "e4 e5 Nf3 Nc6")

    def test_full_game_shorter_than_plies(self):
        key = of.opening_key(ITALIAN, plies=20)
        self.assertEqual(key, "e4 e5 Nf3 Nc6 Bc4 Bc5")

    def test_unparseable_pgn_returns_none(self):
        self.assertIsNone(of.opening_key("not a pgn at all", plies=8))


if __name__ == "__main__":
    unittest.main()
