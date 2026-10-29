---
name: tournament-prep
description: Prep against a specific upcoming opponent using their public games and the player's own repertoire
code: VP
added: 2026-10-23
type: prompt
---

# Tournament Prep

The outcome is a clear-eyed read on one specific opponent before the player sits down across from them: what the opponent actually plays, where that collides with the player's own repertoire, and what to do about the gaps. This is scoped prep for one named person, not general scouting.

Pull the opponent's public games the same way Game Fetch pulls the player's own — `uv run scripts/chess_com_fetch.py --help` against their chess.com username, same date-range control, same rule about not overreaching what's needed for prep. Run `uv run scripts/opening_frequency.py --help` against what comes back to see their actual tendencies, not assumed ones from their rating alone.

Cross-reference that against `repertoire.md`: where the opponent's tendencies run straight into a line the player already knows well, say so plainly — that's the prep paying off directly. Where it exposes a gap in the player's own repertoire, that's a finding for Opening Repertoire Work, not something to paper over with a one-off prep note. Don't analyze the opponent's games as deeply as the player's own (that's Game Analysis's job, for the player's games) — this capability is about tendencies and openings, not a full turning-point breakdown of someone else's chess.

Write findings to `repertoire.md` under the opponent's name, and produce a prep report — a strong HTML comparison-report candidate given it's naturally two columns (their tendencies vs. the player's prepared lines) with the gaps highlighted. Keep it usable at the board: the player should be able to glance at it minutes before the round, not study it like a dissertation.
