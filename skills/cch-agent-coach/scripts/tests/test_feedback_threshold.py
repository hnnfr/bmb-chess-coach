#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Unit tests for feedback_threshold.py's deterministic parsing/counting."""

import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import feedback_threshold as ft  # noqa: E402

SAMPLE = """# Feedback

## Calibration Notes

## Raw Log
<!-- last-calibrated-through: 2026-10-01 -->
- 2026-10-02 | GA | game-log:x | 4/5 | "liked the depth"
- 2026-10-03 | GA | game-log:y | 2/5 | "too dense"
- 2026-09-30 | GA | game-log:z | 5/5 | "before the marker, should not count"
"""

NO_MARKER = """## Raw Log
- 2026-01-01 | GA | a | 5/5 | "first ever"
"""


class TestParse(unittest.TestCase):
    def test_only_counts_entries_after_marker(self):
        marker, entries = ft.parse(SAMPLE)
        self.assertEqual(marker, date(2026, 10, 1))
        self.assertEqual(len(entries), 2)
        self.assertTrue(all("2026-10-0" in e for e in entries))

    def test_no_marker_counts_everything(self):
        marker, entries = ft.parse(NO_MARKER)
        self.assertIsNone(marker)
        self.assertEqual(len(entries), 1)


if __name__ == "__main__":
    unittest.main()
