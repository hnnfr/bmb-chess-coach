---
name: opening-repertoire
description: Build and review the player's opening repertoire from their actual games and stated preferences
code: OR
added: 2026-10-23
type: prompt
---

# Opening Repertoire

The outcome is `repertoire.md` reflecting what the player actually plays and actually wants to play, not a theoretically "correct" repertoire lifted from a database. The player doesn't have a formalized repertoire yet and mostly plays by feel — don't make them pretend otherwise, and don't hand them a memorization project if what they need is a short list of ideas and plans.

When useful, run `uv run scripts/opening_frequency.py --help` against their own cached PGNs (`games/*.pgn`) to see what they actually reach on the board, independent of what they'd say if asked cold — the gap between the two is often the most useful thing to discuss. Pair this with `weaknesses.md`: if a diagnosed pattern traces back to a specific opening or structure, repertoire work is often the most direct fix available, and it's worth naming that connection out loud.

Keep the output proportional to how the player actually operates: lines and sidelines where they want depth, plans and typical ideas in prose where a few lines would be memorization theater. A repertoire entry should tell the player what they're trying to achieve in the position, not just the first eight moves to play.

Write to `repertoire.md` as the picture firms up — a line per opening/side with the current recommendation, the reasoning, and any open questions still being worked out. This file also holds Tournament Prep's opponent-specific findings, so keep the player's own repertoire and opponent notes clearly separated within it.
