# Weaknesses

_Curated, evolving library of recurring patterns — promoted from candidates (single-game observations) to confirmed (seen across multiple analyzed games) once Weakness Diagnosis has run a batch._

## Candidates (from single games — not yet confirmed as recurring)

### Plan commitment without threat-verification
First seen: 2026-10-09 game vs jawzy14 (Black, resigned).

Three of five turning points in this game trace to the same root: Hongnam commits to an idea (attack the bishop, protect the king, deny a square) without checking it against what's concretely happening on the board at that moment.
- **g5** (move 7): reacted to the opponent's bishop being attackable, ignored his own undeveloped g8-knight. Pure reflex, no real plan.
- **Kd7** (move 13): correctly diagnosed the danger (connected rooks after O-O-O) but walked the king onto the exact open file the danger was on.
- **f5** (move 26): the most advanced version — this one had a real, partially correct plan (deny Ne4, free f6 for the knight), but missed a bigger threat one square further down the same diagonal (Nd5→Nb6+ fork). Refined conclusion: not pure reflex anymore, but **doesn't triage multiple candidate threats by how much they actually cost** — answered a threat worth a pawn, missed one worth a rook.

This connects directly to the fixed-opening-skeleton pattern from First Breath (BOND.md) — same root behavior (commit to a shape, push toward it regardless of resistance) showing up mid-game under a different costume.

**Status:** one game is not a pattern. Watch for this across the next few analyzed games before calling it confirmed.
