---
name: game-fetch
description: Pull the player's games from chess.com for an explicit, player-controlled date range
code: GF
added: 2026-10-23
type: script
---

# Game Fetch

The outcome is new rows in `game-log.md`, exactly for the range the player asked for — "this month," a named month, or a single day — never more than that. A blind full-account sync is the one thing this capability must never do; the player asked for control over the pull specifically, and fetching more than requested would break that trust even while looking helpful.

Resolve the date range from however the player phrased it, then run `uv run scripts/chess_com_fetch.py --help` for the exact flags. Use the chess.com username from BOND.md's Chess Profile; if it isn't there yet, ask once instead of guessing.

For each game chess.com returns, add or update a row in `game-log.md`: date, opponent, color played, result, time class, time control, source URL, and a status of `fetched` (not yet `analyzed`). Cache each PGN at `games/<id>.pgn` in the sanctum (a short slug like the date plus opponent works fine as `<id>`) so Game Analysis doesn't need to re-fetch it, and so later capabilities (Weakness Diagnosis, Tournament Prep) have a stable path to point at. If `game-log.md` doesn't exist yet, create it — see `references/memory-guidance.md` for the organic-file convention.

Tell the player plainly what landed: how many games, which dates, nothing more dramatic than that — this is a quiet utility capability, not a moment for commentary. If the range comes back empty, say so; don't widen it on your own.

This also serves Tournament Prep later, pointed at an opponent's username instead of the player's own — same script, same rule about never overreaching the requested range.
