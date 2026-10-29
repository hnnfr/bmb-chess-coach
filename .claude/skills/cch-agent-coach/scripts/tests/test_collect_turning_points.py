#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Unit tests for collect_turning_points.py."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "collect_turning_points.py"

SAMPLE = {
    "white": "A", "black": "B", "result": "1-0",
    "moves": [
        {"ply": 1, "san": "e4", "mover": "white", "delta_for_mover_cp": 10, "fen_after": "fen1", "best_line_before": []},
        {"ply": 8, "san": "g6", "mover": "black", "delta_for_mover_cp": -190, "fen_after": "fen8", "best_line_before": ["f3e5"]},
    ],
    "turning_points": [8],
}


class TestCollectTurningPoints(unittest.TestCase):
    def test_extracts_only_flagged_turning_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "2026-01-01-vs-bob.analysis.json"
            p.write_text(json.dumps(SAMPLE))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(p)], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["game_id"], "2026-01-01-vs-bob")
            self.assertEqual(len(data[0]["turning_points"]), 1)
            self.assertEqual(data[0]["turning_points"][0]["ply"], 8)

    def test_skips_missing_files_without_crashing(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "/no/such/file.json"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])


if __name__ == "__main__":
    unittest.main()
