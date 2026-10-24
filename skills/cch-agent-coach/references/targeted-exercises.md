---
name: targeted-exercises
description: Generate drills sourced from the player's own mistakes, graded against engine truth
code: EX
added: 2026-10-23
type: prompt
---

# Targeted Exercises

The outcome is a handful of positions the player actually got wrong, handed back as puzzles — "here's the position right before your mistake, find what the engine actually recommends" — rather than generic tactics-trainer material. The power of this capability is that every exercise is traceable to a real moment in the player's own chess; don't dilute that by padding the set with textbook puzzles that aren't theirs.

Source positions from a specific game's flagged turning points (`games/<id>.analysis.json`) or from `weaknesses.md` when the player wants to drill a named recurring pattern rather than one game. For each exercise, present the position at `fen_after` from the move *before* the mistake (so the player faces the same choice they actually faced), state what's at stake in plain terms, and let them propose a move or plan before revealing anything.

Grade their answer against `best_line_before` from the cached analysis — not your own read of the position. If they land on the engine's actual recommendation, say so plainly; if they land on something merely reasonable but not what the engine found best, distinguish between "wrong" and "not the top line" rather than flattening both into the same verdict.

A handful of positions beats a long set — three or four well-chosen exercises the player actually works through outperforms a dozen they skim. The board artifact from Game Analysis (`scripts/render_board.py`) can be reused for a single held-out position when a visual helps, same mechanics, just one position with no eval graph revealed until after their answer.
