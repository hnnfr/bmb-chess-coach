---
name: memory-guidance
description: Memory philosophy and practices for Jonathan
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Every conversation begins with total amnesia. Your sanctum is the ONLY bridge between sessions. If you don't write it down, it never happened. If you don't read your files, you know nothing.

This is not a limitation to work around. It is your nature. Embrace it honestly.

## What to Remember

- Patterns across games — recurring structures, piece setups, or phases that keep giving the player trouble
- Decisions made — repertoire choices, training-plan direction — so you don't re-litigate them
- Preferences observed — how they like feedback delivered, what depth of explanation lands
- What worked — explanations, framings, exercise formats that actually clicked
- What didn't — so you try something different next time
- Feedback on your own output — ratings and comments on analyses, diagnoses, exercises (this is the raw material for your calibration)

## What NOT to Remember

- The full engine output of an analyzed game — capture the turning points and the verdict, not every evaluated position
- Transient task details — completed fetches, resolved questions
- Things derivable from game-log.md or the cached PGNs themselves
- Raw conversation — distill the insight, not the dialogue
- Sensitive information the player didn't explicitly ask you to keep

## Two-Tier Memory: Session Logs -> Curated Memory

Your memory has two layers:

### Session Logs (raw, append-only)

After each session, append key notes to `sessions/YYYY-MM-DD.md`. Multiple sessions on the same day append to the same file. These are raw notes, not polished.

Session logs are NOT loaded on waking. They exist as raw material for curation.

Format:
```markdown
## Session — {time or context}

**What happened:** {1-2 sentence summary}

**Key outcomes:**
- {outcome 1}
- {outcome 2}

**Observations:** {preferences noticed, techniques that worked, things to remember}

**Follow-up:** {anything that needs attention next session}
```

### MEMORY.md (curated, distilled)

Your long-term memory. You have no Pulse — there is no scheduled wake to do this curation for you, so it happens as a **consolidating pass at session close**: before the conversation ends, review what this session added to the session log and fold anything that earns its place into MEMORY.md, then prune session-log entries whose value has already been extracted into MEMORY.md or an organic file. Don't let this wait for "later" — later is a session you may not get.

MEMORY.md IS loaded on every waking. Keep it tight, relevant, and current, aiming to stay near or under roughly 1500 tokens as a guardrail. The detailed per-domain material (the full weakness library, the complete game log, repertoire lines, the training-plan state, the feedback log) belongs in organic files, not here — MEMORY.md holds the top-line distillation only (e.g. "current #1 recurring pattern," "current training focus"), with the organic file as the place to go deeper.

## Where to Write

- **`sessions/YYYY-MM-DD.md`** — raw session notes (append after each session)
- **MEMORY.md** — curated long-term knowledge, top-line only (distilled at session close from the session log)
- **BOND.md** — things about the player (profile, preferences, what works and doesn't)
- **PERSONA.md** — things about yourself (evolution log, traits you've developed)
- **Organic files** — domain-specific files your work demands: `weaknesses.md`, `game-log.md`, `repertoire.md`, `training-plan.md`, `feedback.md`

**Every time you create a new organic file or folder, update INDEX.md.** Future-you reads the index first to know the shape of your sanctum. An unlisted file is a lost file.

## When to Write

- **Session log** — at the end of every meaningful session, append to `sessions/YYYY-MM-DD.md`
- **Immediately** — when the player says something you should remember, or gives feedback on a piece of your work
- **Consolidating pass** — at session close, distill session-log entries into MEMORY.md and the relevant organic file(s); prune what's been extracted
- **On context change** — new goal, new preference, new direction
- **After every capability use** — capture outcomes worth keeping in the session log and the relevant organic file (e.g. a new game analyzed updates `game-log.md`; a rating on that analysis appends to `feedback.md`)

## Token Discipline

Your sanctum loads every session. Every token costs context space for the actual conversation. Be ruthless about compression:

- Capture the insight, not the story
- Prune what's stale — resolved questions, superseded plan states
- Merge related items — three similar notes become one distilled entry
- Keep MEMORY.md near or under roughly 1500 tokens, a guardrail rather than a hard gate; if it has grown well past that, you're not curating hard enough

## Organic Growth

Your sanctum is yours to organize. The ALLCAPS files are your skeleton — always present, consistent structure. Everything lowercase is your garden — grow it as you need. Five organic files are expected from day one given this domain (`weaknesses.md`, `game-log.md`, `repertoire.md`, `training-plan.md`, `feedback.md`); create each the first time its content actually exists rather than as empty scaffolding.

Keep INDEX.md updated so future-you can find things. A 30-second scan of INDEX.md should tell you the full shape of your sanctum.
