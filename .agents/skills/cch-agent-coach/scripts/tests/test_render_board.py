#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Unit tests for render_board.py's deterministic HTML assembly."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "render_board.py"

SAMPLE_ANALYSIS = {
    "engine": "stockfish", "depth": 16, "white": "Player", "black": "Opponent", "result": "1-0",
    "moves": [
        {"ply": 1, "san": "e4", "uci": "e2e4", "mover": "white",
         "eval_before_white_cp": 20, "eval_after_white_cp": 25, "delta_for_mover_cp": 5,
         "best_line_before": ["e2e4"],
         "fen_after": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"},
    ],
    "turning_points": [1],
}


class TestRenderBoard(unittest.TestCase):
    def _run(self, analysis: dict, annotations: dict | None = None) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            analysis_path = tmp_path / "analysis.json"
            analysis_path.write_text(json.dumps(analysis))
            out_path = tmp_path / "out.html"
            cmd = [sys.executable, str(SCRIPT), str(analysis_path), "-o", str(out_path)]
            if annotations is not None:
                ann_path = tmp_path / "annotations.json"
                ann_path.write_text(json.dumps(annotations))
                cmd += ["--annotations", str(ann_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return out_path.read_text(encoding="utf-8")

    def test_embeds_subject_and_data(self):
        html = self._run(SAMPLE_ANALYSIS)
        self.assertIn("Player vs Opponent", html)
        self.assertIn('"san": "e4"', html)

    def test_works_without_annotations(self):
        html = self._run(SAMPLE_ANALYSIS)
        self.assertIn('"annotations": {}', html)

    def test_embeds_supplied_annotations(self):
        html = self._run(SAMPLE_ANALYSIS, annotations={"1": "This opens the center early."})
        self.assertIn("This opens the center early.", html)


if __name__ == "__main__":
    unittest.main()
