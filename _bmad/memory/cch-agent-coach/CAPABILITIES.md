# Capabilities

## Built-in

| Code | Name | Description | Source |
|------|------|-------------|--------|
| [CC] | coach-self-calibration | Review accumulated feedback and distill it into calibration notes that reshape future coaching | `references/coach-self-calibration.md` |
| [GA] | game-analysis | Deep, engine-grounded analysis of one game's 3-5 turning points, interactive or written | `references/game-analysis.md` |
| [GF] | game-fetch | Pull the player's games from chess.com for an explicit, player-controlled date range | `references/game-fetch.md` |
| [OR] | opening-repertoire | Build and review the player's opening repertoire from their actual games and stated preferences | `references/opening-repertoire.md` |
| [EX] | targeted-exercises | Generate drills sourced from the player's own mistakes, graded against engine truth | `references/targeted-exercises.md` |
| [VP] | tournament-prep | Prep against a specific upcoming opponent using their public games and the player's own repertoire | `references/tournament-prep.md` |
| [TP] | training-plan | A self-paced training plan that adapts to irregular availability, with no calendar assumption | `references/training-plan.md` |
| [WD] | weakness-diagnosis | Mine a batch of analyzed games for emergent, recurring patterns across games | `references/weakness-diagnosis.md` |

## Learned

_Capabilities added by the owner over time. Prompts live in `capabilities/`._

| Code | Name | Description | Source | Added |
|------|------|-------------|--------|-------|

## How to Add a Capability

Tell me "I want you to be able to do X" and we'll create it together.
I'll write the prompt, save it to `capabilities/`, and register it here.
Next session, I'll know how.
Load `references/capability-authoring.md` for the full creation framework.

## Tools

Prefer crafting your own tools over depending on external ones. A script you wrote and saved is more reliable than an external API. Use the file system creatively.

### User-Provided Tools

- **Local Stockfish:** installed at `C:\HNN\Apps\stockfish` — use this installation rather than assuming a bundled/default path.
