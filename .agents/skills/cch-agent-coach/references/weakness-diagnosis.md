---
name: weakness-diagnosis
description: Mine a batch of analyzed games for emergent, recurring patterns across games
code: WD
added: 2026-10-23
type: prompt
---

# Weakness Diagnosis

The outcome is `weaknesses.md` gaining (or reinforcing) a pattern the player didn't already have named precisely — the structural, positional, or tactical thing that actually recurs, not a label imposed because it's a well-known category. The player was explicit that this is open-ended: don't walk in with a checklist of weakness types to confirm. Whatever shows up in the games is the finding, even if it's narrower or stranger than any textbook category — "discomfort in queen-and-bishop-battery positions specifically" is exactly the shape of thing to surface, not to round off into "tactical awareness."

Resolve which games are in scope from however the player phrased the batch (a count, a date range, "everything since my last diagnosis") against `game-log.md`, restricted to entries with status `analyzed`. Run `uv run scripts/collect_turning_points.py --help` against their cached `games/<id>.analysis.json` files — it pulls just the flagged turning points out of each game instead of handing you every full analysis to read cover to cover. Look across what comes back for what repeats: a recurring pawn structure, a piece configuration the player keeps mishandling, a phase of the game, a motif. One game is an anecdote; three or more independent games showing the same thing is a pattern worth naming.

Weigh games the way the player actually does: they consider anything under 30 minutes lower-signal for real thinking, so a pattern that only shows up in bullet games is weaker evidence than the same pattern in their longer games — say so rather than treating every game as equally diagnostic.

Write confirmed patterns to `weaknesses.md`, each with a name, a short description of the mechanism (not just "struggles with X"), and references to the games/plies that support it. If a pattern already exists there, strengthen or refine it rather than duplicating — note the new supporting evidence and update the description if this batch sharpened your understanding of it.

Close with a summary the player can actually act on, not a wall of data. This is a strong candidate for an HTML dashboard: patterns ranked by how often they recur, with links to the specific games and positions that demonstrate each one — build one if the batch is large enough to benefit from it (roughly five or more games); for a small batch, a short written summary is enough.
