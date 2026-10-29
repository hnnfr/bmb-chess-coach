#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Count raw feedback entries since the last calibration pass, and say whether
Coach Self-Calibration should fire.

Deterministic by construction (same feedback.md content always yields the
same count), which is why counting lives here instead of being an LLM's
running tally -- an exact threshold trigger needs an exact count, not a
"does this feel like about enough feedback" judgment call.

Expects feedback.md in this shape:

    ## Raw Log
    <!-- last-calibrated-through: 2026-10-01 -->
    - 2026-10-02 | GA | game-log:2026-10-01-vs-bob | 4/5 | "liked the depth"
    - 2026-10-05 | WD | ... | 2/5 | "too dense, wanted top 3 not top 10"

A log entry line starts with "- YYYY-MM-DD". The marker comment holds the
date through which feedback has already been folded into calibration notes;
entries dated after it are "new." If the marker is missing, every entry
counts as new (first calibration pass).

Usage:
    uv run feedback_threshold.py <feedback.md> [--threshold N] [-o OUTPUT]

Exit codes: 0 = below threshold, 1 = threshold met, 2 = usage/file error.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

MARKER_RE = re.compile(r"<!--\s*last-calibrated-through:\s*(\d{4}-\d{2}-\d{2})\s*-->")
ENTRY_RE = re.compile(r"^-\s*(\d{4}-\d{2}-\d{2})\s*\|")


def parse(text: str) -> tuple[date | None, list[str]]:
    marker_match = MARKER_RE.search(text)
    marker = date.fromisoformat(marker_match.group(1)) if marker_match else None

    entries = []
    for line in text.splitlines():
        m = ENTRY_RE.match(line.strip())
        if not m:
            continue
        entry_date = date.fromisoformat(m.group(1))
        if marker is None or entry_date > marker:
            entries.append(line.strip())
    return marker, entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("feedback_file", help="Path to feedback.md")
    parser.add_argument("--threshold", type=int, default=5, help="Entries needed to trigger calibration (default: 5)")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    path = Path(args.feedback_file)
    if not path.exists():
        print(f"No feedback file at {path} -- nothing to calibrate from yet.", file=sys.stderr)
        return 2

    marker, entries = parse(path.read_text(encoding="utf-8"))
    threshold_met = len(entries) >= args.threshold
    result = {
        "last_calibrated_through": marker.isoformat() if marker else None,
        "new_entry_count": len(entries),
        "threshold": args.threshold,
        "threshold_met": threshold_met,
        "new_entries": entries,
    }

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    print(f"{len(entries)}/{args.threshold} new feedback entries.", file=sys.stderr)
    return 1 if threshold_met else 0


if __name__ == "__main__":
    raise SystemExit(main())
