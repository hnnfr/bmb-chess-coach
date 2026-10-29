#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Pre-pass for Weakness Diagnosis: pull just the turning-point moves out of a
batch of already-analyzed games, instead of handing the model every full
per-move analysis file to read cover to cover.

Deterministic extraction (same files in, same compact array out), which is
why this is a script rather than asking the model to skim N large JSON files
itself. The model still does the actual pattern-naming -- this just gets it
a small, consistent slice of evidence to look at across games.

Usage:
    uv run collect_turning_points.py <analysis.json> [<analysis.json> ...] [-o OUTPUT]

Each input is one chess_engine.py analysis file (produced by Game Analysis
and cached at games/<id>.analysis.json). The game id is taken from the
filename stem (minus a trailing ".analysis").
"""

import argparse
import json
import sys
from pathlib import Path


def game_id_from_path(path: Path) -> str:
    stem = path.stem
    return stem[:-len(".analysis")] if stem.endswith(".analysis") else stem


def extract(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    moves_by_ply = {m["ply"]: m for m in data.get("moves", [])}
    turning = []
    for ply in data.get("turning_points", []):
        m = moves_by_ply.get(ply)
        if not m:
            continue
        turning.append({
            "ply": ply,
            "san": m["san"],
            "mover": m["mover"],
            "delta_for_mover_cp": m["delta_for_mover_cp"],
            "fen_after": m["fen_after"],
            "best_line_before": m.get("best_line_before", []),
        })
    return {
        "game_id": game_id_from_path(path),
        "white": data.get("white", "?"),
        "black": data.get("black", "?"),
        "result": data.get("result", "?"),
        "turning_points": turning,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("analysis_files", nargs="+", help="One or more games/<id>.analysis.json paths")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    collected = []
    for raw in args.analysis_files:
        path = Path(raw)
        if not path.exists():
            print(f"Skipping missing file: {path}", file=sys.stderr)
            continue
        collected.append(extract(path))

    output = json.dumps(collected, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    print(f"Collected turning points from {len(collected)} game(s).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
