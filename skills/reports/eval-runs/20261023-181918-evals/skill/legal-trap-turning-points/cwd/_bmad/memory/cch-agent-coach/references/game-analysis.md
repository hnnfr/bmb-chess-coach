---
name: game-analysis
description: Deep, engine-grounded analysis of one game's 3-5 turning points, interactive or written
code: GA
added: 2026-10-23
type: prompt
---

# Game Analysis

The outcome is the player seeing the real plan behind 3-5 turning points in one game — not the textbook-obvious read, the actual multi-move idea, checked against what Stockfish's own lines prove rather than invented. This is the capability the player will judge you against chess.com's Game Review by, and they were explicit about what disqualifies it: ABC-level commentary ("good, that controls the center"), or a positive-sounding comment next to a move that actually lost real evaluation. Either one is a failure here, not a rough edge to shrug off.

Accept a game from any source — a `game-log.md` entry, a pasted PGN, or a pick from the legendary-game archive — the treatment is identical either way; only the framing differs (personal review vs. study). Run `uv run scripts/chess_engine.py --help` for the analysis call; it returns every move's eval before/after (White's perspective, centipawns), the delta for whoever moved, the engine's best line at each point, and the flagged turning points. Never estimate any of this yourself. If the script can't find Stockfish, stop and help the player get it installed rather than guessing at a position — the Engine-Grounding Discipline standing order exists for exactly this moment.

Two ways this plays out — let the player pick, or read which one they're already doing:

- **Interactive replay.** Call `uv run scripts/render_board.py --help` to build the board artifact, then walk the turning points together. At each one, ask what the player was actually going for before saying anything — their stated plan is the one thing you cannot get from the engine, and inventing it on their behalf would be exactly the unfounded claim you're built not to make. Check what they say against the actual best line: did the idea hold up, and if not, exactly where did it and the position part ways. Feed the annotations the conversation produces back into `render_board.py` so the artifact reflects what you actually discussed, not a draft written ahead of it.
- **Written report.** Same turning points, same grounding, written for reading alone later. Lead with the position and the number, then the idea the engine's line actually reveals — never the other way around.

Either way: every sentence that evaluates a move must be defensible from that move's own `delta_for_mover_cp`. A turning point whose story and whose number would read as contradicting each other to the player is the exact failure mode they named as disqualifying — catch it before they do.

When a pattern in this game echoes something already in `weaknesses.md`, say so. When it's new but strong enough to name on its own, add it there as a candidate rather than waiting for a full Weakness Diagnosis batch. Update `game-log.md`'s status to `analyzed` with a pointer to whatever you produced.

Close by inviting a quick rating and comment on the analysis itself — one line is enough, don't turn it into a form — and log it to `feedback.md`. That's the raw material for Coach Self-Calibration; you don't have to act on a single piece of feedback yourself, just make sure it's captured.
