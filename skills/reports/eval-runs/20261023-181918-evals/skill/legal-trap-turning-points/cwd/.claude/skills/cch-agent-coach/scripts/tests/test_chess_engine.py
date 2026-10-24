#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["chess>=1.10"]
# ///
"""Unit tests for the deterministic (non-engine) parts of chess_engine.py."""

import sys
import unittest
from pathlib import Path

import chess
import chess.engine

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import chess_engine as ce  # noqa: E402


class TestFindStockfish(unittest.TestCase):
    def test_explicit_path_must_exist(self):
        self.assertIsNone(ce.find_stockfish("/definitely/not/a/real/path/stockfish"))

    def test_no_path_falls_back_to_which_or_none(self):
        # Can't assert a specific result (depends on the test machine), only that
        # it doesn't raise and returns either None or a string.
        result = ce.find_stockfish(None)
        self.assertTrue(result is None or isinstance(result, str))


class TestScoreToCp(unittest.TestCase):
    def test_plain_cp_score(self):
        score = chess.engine.PovScore(chess.engine.Cp(42), chess.WHITE)
        self.assertEqual(ce.score_to_cp(score), 42)

    def test_negative_cp_score_from_black_pov_normalizes_to_white(self):
        # 30cp good for Black == -30 from White's perspective.
        score = chess.engine.PovScore(chess.engine.Cp(30), chess.BLACK)
        self.assertEqual(ce.score_to_cp(score), -30)

    def test_mate_score_collapses_to_large_finite_value(self):
        score = chess.engine.PovScore(chess.engine.Mate(3), chess.WHITE)
        cp = ce.score_to_cp(score)
        self.assertGreater(cp, 5000)
        self.assertLess(cp, ce.MATE_SCORE_CP)

    def test_mate_against_mover_is_negative(self):
        score = chess.engine.PovScore(chess.engine.Mate(-2), chess.WHITE)
        self.assertLess(ce.score_to_cp(score), -5000)


if __name__ == "__main__":
    unittest.main()
