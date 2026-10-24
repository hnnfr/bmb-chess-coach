#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Fetch a player's games from chess.com's public API for an explicit date range.

Deterministic by design: same username + date range always yields the same
games (chess.com archives are immutable once a month closes). This is why it
is a script and not a prompt — Jonathan asks the player for a range, this
script does the exact fetch, and the capability narrates what came back.

chess.com exposes monthly archives only (no single-day endpoint), so a
single-day or partial-month request fetches that month's archive and filters
client-side by end_time. No authentication is required for public archives.

Usage:
    uv run chess_com_fetch.py <username> --from YYYY-MM-DD --to YYYY-MM-DD
    uv run chess_com_fetch.py <username> --month YYYY-MM
    uv run chess_com_fetch.py <username> --on YYYY-MM-DD

Output: JSON array to stdout (or -o file), one entry per game:
    {end_time, url, time_class, time_control, white, black, result, pgn}
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone

API_BASE = "https://api.chess.com/pub/player"
USER_AGENT = "cch-agent-coach/1.0 (chess coaching module; contact via chess.com profile)"


def month_range(start: date, end: date):
    """Yield (year, month) for every calendar month the [start, end] range touches."""
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        yield y, m
        m += 1
        if m > 12:
            m = 1
            y += 1


def fetch_month(username: str, year: int, month: int) -> list[dict]:
    url = f"{API_BASE}/{username}/games/{year:04d}/{month:02d}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []  # no games that month
        raise
    return data.get("games", [])


def to_entry(game: dict) -> dict:
    end = datetime.fromtimestamp(game.get("end_time", 0), tz=timezone.utc)
    white = game.get("white", {})
    black = game.get("black", {})
    return {
        "end_time": end.isoformat(),
        "url": game.get("url", ""),
        "time_class": game.get("time_class", ""),
        "time_control": game.get("time_control", ""),
        "white": {"username": white.get("username", ""), "result": white.get("result", "")},
        "black": {"username": black.get("username", ""), "result": black.get("result", "")},
        "pgn": game.get("pgn", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("username", help="chess.com username to fetch games for")
    parser.add_argument("--from", dest="date_from", help="Range start, YYYY-MM-DD")
    parser.add_argument("--to", dest="date_to", help="Range end, YYYY-MM-DD")
    parser.add_argument("--month", help="A single calendar month, YYYY-MM")
    parser.add_argument("--on", help="A single day, YYYY-MM-DD")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.month:
        y, m = (int(p) for p in args.month.split("-"))
        start = date(y, m, 1)
        end = date(y, m + 1, 1) if m < 12 else date(y + 1, 1, 1)
    elif args.on:
        start = end = date.fromisoformat(args.on)
    elif args.date_from and args.date_to:
        start = date.fromisoformat(args.date_from)
        end = date.fromisoformat(args.date_to)
    else:
        print("Specify one of: --month YYYY-MM | --on YYYY-MM-DD | --from ... --to ...", file=sys.stderr)
        return 2

    start_dt = datetime(start.year, start.month, start.day, tzinfo=timezone.utc)
    end_dt = datetime(end.year, end.month, end.day, 23, 59, 59, tzinfo=timezone.utc)

    games: list[dict] = []
    for y, m in month_range(start, end):
        if args.verbose:
            print(f"Fetching {args.username} {y:04d}-{m:02d}...", file=sys.stderr)
        try:
            raw = fetch_month(args.username, y, m)
        except urllib.error.URLError as e:
            print(f"Network error fetching {y:04d}-{m:02d}: {e}", file=sys.stderr)
            return 1
        for g in raw:
            end_time = datetime.fromtimestamp(g.get("end_time", 0), tz=timezone.utc)
            if start_dt <= end_time <= end_dt:
                games.append(to_entry(g))

    games.sort(key=lambda g: g["end_time"])
    output = json.dumps(games, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)
    print(f"{len(games)} game(s) in range.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
