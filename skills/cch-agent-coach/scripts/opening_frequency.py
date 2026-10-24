#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["chess>=1.10"]
# ///
"""
Tally how often each opening move sequence appears across a batch of PGNs.

Deterministic counting -- same PGNs in, same frequency table out -- used by
both Opening Repertoire Work (the player's own games: what do I actually
play?) and Tournament Prep (an opponent's games: what do they actually
play?). The model's job is deciding what the frequency table means for
repertoire or prep; this script only produces the table.

Usage:
    uv run opening_frequency.py <pgn-file> [<pgn-file> ...] [--plies N] [--side white|black|both] [-o OUTPUT]

--plies caps how many half-moves define "the opening" for grouping purposes
(default 8, i.e. 4 full moves). --side filters which player's games count,
useful when a PGN set mixes both colors for the same person.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import chess.pgn


def opening_key(pgn_text: str, plies: int) -> str | None:
    game = chess.pgn.read_game(__import__("io").StringIO(pgn_text))
    if game is None:
        return None
    board = game.board()
    sans = []
    for i, move in enumerate(game.mainline_moves()):
        if i >= plies:
            break
        sans.append(board.san(move))
        board.push(move)
    return " ".join(sans) if sans else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pgn_files", nargs="+", help="One or more PGN file paths")
    parser.add_argument("--plies", type=int, default=8, help="Half-moves to group by (default: 8)")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    counter: Counter[str] = Counter()
    total = 0
    skipped = 0
    for raw in args.pgn_files:
        path = Path(raw)
        if not path.exists():
            print(f"Skipping missing file: {path}", file=sys.stderr)
            continue
        key = opening_key(path.read_text(encoding="utf-8"), args.plies)
        if key is None:
            skipped += 1
            continue
        counter[key] += 1
        total += 1

    table = [
        {"opening": k, "count": c, "frequency": round(c / total, 3) if total else 0.0}
        for k, c in counter.most_common()
    ]
    result = {"games_counted": total, "games_skipped": skipped, "plies": args.plies, "openings": table}

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    print(f"Tallied {total} game(s) into {len(table)} distinct opening(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
