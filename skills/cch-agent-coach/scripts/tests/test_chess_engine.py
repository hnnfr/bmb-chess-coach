#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["chess>=1.10"]
# ///
"""Unit tests for the deterministic (non-engine) parts of chess_engine.py."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

import chess
import chess.engine

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import chess_engine as ce  # noqa: E402


def _make_fake_binary(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\necho fake\n")
    path.chmod(0o755)


class TestFindStockfish(unittest.TestCase):
    def test_explicit_path_must_exist(self):
        self.assertIsNone(ce.find_stockfish("/definitely/not/a/real/path/stockfish"))

    def test_no_path_falls_back_to_which_or_none(self):
        # Can't assert a specific result (depends on the test machine), only that
        # it doesn't raise and returns either None or a string.
        result = ce.find_stockfish(None)
        self.assertTrue(result is None or isinstance(result, str))


class TestGlobForStockfish(unittest.TestCase):
    def test_finds_versioned_filename_directly_in_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            binary = base / "stockfish-windows-x86-64-avx2.exe"
            _make_fake_binary(binary)
            found = ce._glob_for_stockfish(base, depth=0)
            self.assertEqual([p.name for p in found], [binary.name])

    def test_finds_nested_one_level_down(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            binary = base / "Stockfish 16" / "stockfish-16.1"
            _make_fake_binary(binary)
            self.assertEqual(ce._glob_for_stockfish(base, depth=0), [])
            found = ce._glob_for_stockfish(base, depth=1)
            self.assertEqual([p.name for p in found], [binary.name])

    def test_missing_base_dir_returns_empty(self):
        self.assertEqual(ce._glob_for_stockfish(Path("/no/such/directory/at/all"), depth=2), [])

    def test_non_executable_match_excluded_where_permissions_are_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            binary = base / "stockfish-not-executable"
            binary.write_text("not actually a binary")
            binary.chmod(0o644)
            found = ce._glob_for_stockfish(base, depth=0)
            if os.name != "nt":
                # Windows' os.access(X_OK) doesn't reflect POSIX exec bits the
                # same way, so this assertion only holds on POSIX platforms.
                self.assertEqual(found, [])


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
