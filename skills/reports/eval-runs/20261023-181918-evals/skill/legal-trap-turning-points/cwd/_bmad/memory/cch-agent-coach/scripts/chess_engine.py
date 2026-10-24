#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["chess>=1.10"]
# ///
"""
Ground-truth game analysis via python-chess + a local Stockfish engine.

This is the non-negotiable: Jonathan never evaluates a position himself. This
script is the only source of truth for legality, evaluation, and best lines.
It is deterministic by construction (same PGN + same engine settings always
produce the same numbers), which is exactly why it is a script and not a
judgment the model makes.

For each move played, it records the engine evaluation before and after (from
White's perspective, in centipawns; mate scores collapse to a large finite
value so deltas stay comparable) and the delta from the mover's perspective
(negative = the position got worse for whoever just moved). It then flags the
N largest-magnitude negative deltas as turning points and attaches the
engine's best line at that position, so the capability prompt has concrete,
grounded material to narrate from instead of inventing it.

Usage:
    uv run chess_engine.py <pgn-file-or-"-"-for-stdin> [--stockfish PATH]
        [--depth N] [--turning-points N] [-o OUTPUT]

Exit codes: 0 = analyzed, 1 = engine/analysis error, 2 = usage error,
3 = Stockfish not found (see stderr for guidance).
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

import chess
import chess.engine
import chess.pgn

MATE_SCORE_CP = 10000


def find_stockfish(explicit: str | None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() else None
    found = shutil.which("stockfish")
    if found:
        return found
    # Common install locations this hunt knows about, checked as a fallback
    # before giving up and asking the player to install it.
    candidates = [
        "/usr/local/bin/stockfish",
        "/usr/bin/stockfish",
        "/opt/homebrew/bin/stockfish",
        "C:\\Program Files\\Stockfish\\stockfish.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def score_to_cp(score: chess.engine.PovScore) -> int:
    """White-perspective centipawns; mate scores collapse to a large finite value."""
    white_score = score.white()
    if white_score.is_mate():
        mate_in = white_score.mate()
        sign = 1 if mate_in > 0 else -1
        return sign * (MATE_SCORE_CP - abs(mate_in))
    return white_score.score()


def analyze(pgn_text: str, stockfish_path: str, depth: int, turning_points: int) -> dict:
    game = chess.pgn.read_game(__import__("io").StringIO(pgn_text))
    if game is None:
        raise ValueError("Could not parse a game from the supplied PGN.")

    board = game.board()
    moves_out = []

    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))
        eval_before = score_to_cp(info["score"])
        best_line_before = [m.uci() for m in info.get("pv", [])][:6]

        for ply, move in enumerate(game.mainline_moves(), start=1):
            mover_is_white = board.turn == chess.WHITE
            san = board.san(move)
            board.push(move)

            info = engine.analyse(board, chess.engine.Limit(depth=depth))
            eval_after = score_to_cp(info["score"])
            best_line_after = [m.uci() for m in info.get("pv", [])][:6]

            # Delta from the mover's own perspective: did their position get
            # better or worse because of the move they just played.
            raw_delta = eval_after - eval_before
            delta_for_mover = raw_delta if mover_is_white else -raw_delta

            moves_out.append({
                "ply": ply,
                "san": san,
                "uci": move.uci(),
                "mover": "white" if mover_is_white else "black",
                "eval_before_white_cp": eval_before,
                "eval_after_white_cp": eval_after,
                "delta_for_mover_cp": delta_for_mover,
                "best_line_before": best_line_before,
                "fen_after": board.fen(),
            })

            eval_before = eval_after
            best_line_before = best_line_after

    ranked = sorted(moves_out, key=lambda m: m["delta_for_mover_cp"])[:turning_points]
    turning_point_plies = sorted(m["ply"] for m in ranked)

    return {
        "engine": "stockfish",
        "depth": depth,
        "white": game.headers.get("White", "?"),
        "black": game.headers.get("Black", "?"),
        "result": game.headers.get("Result", "?"),
        "moves": moves_out,
        "turning_points": turning_point_plies,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pgn", help='Path to a PGN file, or "-" to read PGN from stdin')
    parser.add_argument("--stockfish", help="Path to the Stockfish binary (auto-detected if omitted)")
    parser.add_argument("--depth", type=int, default=16, help="Search depth per position (default: 16)")
    parser.add_argument("--turning-points", type=int, default=5, help="How many turning points to flag (default: 5)")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    stockfish_path = find_stockfish(args.stockfish)
    if not stockfish_path:
        print(
            "Stockfish not found. Pass --stockfish <path>, or install it and ensure it's on PATH.\n"
            "Once you know the path, it should be remembered in CAPABILITIES.md under User-Provided Tools\n"
            "so this never has to be re-resolved.",
            file=sys.stderr,
        )
        return 3

    pgn_text = sys.stdin.read() if args.pgn == "-" else Path(args.pgn).read_text(encoding="utf-8")

    try:
        result = analyze(pgn_text, stockfish_path, args.depth, args.turning_points)
    except Exception as e:  # noqa: BLE001 - surfaced to stderr for the capability to react to
        print(f"Analysis failed: {e}", file=sys.stderr)
        return 1

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    print(f"Analyzed {len(result['moves'])} moves, flagged {len(result['turning_points'])} turning points.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
