---
title: 'Module Plan'
status: 'ideation'
module_name: 'Chess Coach'
module_code: 'cch'
module_description: 'A persistent personal chess coach that uses python-chess and a local Stockfish engine for ground-truth analysis, and an LLM to turn that analysis into human coaching.'
architecture: 'single-agent-with-capabilities'
standalone: true
expands_module: ''
skills_planned: ['cch-agent-coach']
config_variables: []
created: '2026-10-21'
updated: '2026-10-21'
---

# Module Plan

## Vision

<!-- What this module does, who it's for, and why it matters -->

## Architecture

**Decision: single agent with rich capabilities.** `cch-agent-coach` — one persistent Coach persona, one skill. No multi-agent split, no orchestrator.

**Rationale:**
- Every capability (game analysis, pattern diagnosis, repertoire work, exercises, training plan, tournament prep, legendary-game study, game fetch) draws on the *same* accumulated relationship — profile, recurring patterns, repertoire. Splitting into separate agents would fragment that memory for no benefit.
- Multiple agents earn their complexity when domains genuinely need distinct personas or separate memory. Here it's one coaching relationship with many facets, not several domains.
- The underlying Python/python-chess/Stockfish/chess.com-fetch machinery are **tools** the agent calls internally, not separate skills with their own personas.
- Output check passed: the agent's primary role is to *produce* tangible coaching output (analysis, exercises, plans) in every capability — not pure coordination — so no orchestrator is needed.

**Single-skill module implication:** since there's only one skill, config/setup is embedded directly in `cch-agent-coach` rather than needing a separate `-setup` skill (per Create Module's single-skill path).

**Capabilities vs. memory (structural note):** memory files below are the coach's accumulated *knowledge about the player* (state/history). Capabilities are the coach's *actions* (what it knows how to do) — those live as the skill's own instruction files (a main agent file + per-capability instruction files it routes to on demand, mirroring how this module-builder skill itself routes to per-task reference files). Capability briefs are defined in full in the Skills section below.

### Memory Architecture

**Pattern: personal memory only**, internally structured into topic-curated files (no multi-agent shared-memory ceremony needed — single agent, no write concurrency to guard against, so no `daily/` journal layer).

`{project-root}/_bmad/memory/cch-agent-coach/`
- `index.md` — read first on every activation; orients the coach on what exists and recent activity, so it loads selectively rather than everything every session
- `profile.md` — player's general info: rating, chess.com username, goals, time-control preference (default weight toward ≥30-min games)
- `weaknesses.md` — curated, evolving library of the player's recurring patterns/"configurations" (e.g., queen-bishop battery discomfort)
- `game-log.md` — index of every game coach and player have analyzed together (source, date, opponent, result, time control, link to its report)
- `repertoire.md` — the player's game-style information: opening lines, notes, tournament-prep findings on specific opponents
- `training-plan.md` — current flexible/self-paced plan state, reflecting the cadence of coach-player interaction (no calendar assumption)
- `feedback.md` — the coach's two-way improvement loop: curated **calibration notes** (top — distilled adjustments to how the coach approaches analysis/diagnosis/exercises) over a raw, append-only **feedback log** (ratings + comments the player gives after any capability's output)

### Memory Contract

| File | Purpose | Read by | Written by |
| ---- | ------- | ------- | ---------- |
| `index.md` | Orientation — what exists, recent activity | Every capability, on activation | Coach, after any session that touches another curated file |
| `profile.md` | Player's general info and preferences | All capabilities (context) | Init/onboarding (first run); updated when player's goals/rating/username change |
| `weaknesses.md` | Curated recurring patterns/configurations | Game analysis (connect this game to known patterns), exercises, training plan, tournament prep | Weakness diagnosis (primary); game analysis (inline note when a strong one-off pattern is spotted, pending confirmation) |
| `game-log.md` | Index of every analyzed game | Weakness diagnosis (needs the batch), game fetch (avoid re-pulling/re-analyzing), tournament prep | Game fetch (new entries on pull); game analysis (status + report link once analyzed) |
| `repertoire.md` | Opening lines, style notes, opponent-prep findings | Opening repertoire work, tournament prep, game analysis (opening-phase context) | Opening repertoire work, tournament prep |
| `training-plan.md` | Current flexible plan state | Training plan, exercises (what's queued) | Training plan |
| `feedback.md` | Calibration notes + raw feedback log — the coach's two-way improvement loop | All capabilities, on activation (alongside `index.md`) — to calibrate tone/depth/approach before producing output | Every capability (appends a raw rating+comment entry after delivering output); Coach Self-Calibration (distills raw entries into the curated calibration-notes section) |

### Cross-Agent Patterns

Not applicable — single-agent module, no cross-agent handoff.

## Skills

### cch-agent-coach

**Type:** agent

**Persona:** **Jonathan** — named in the spirit of GM Jonathan Rowson's style of deep, principled, psychologically-aware chess thinking. A seasoned, patient club-level coach — not a grandmaster lecturing down, but a sharp training partner who takes your games seriously. Precise and evidence-driven (every claim ties to an engine number), curious about *your* plans before judging them ("what were you going for with this move?"), never condescending, never stops at textbook platitudes. Treats the player as an intermediate-to-strong player who already knows the ABCs — the job is to go past them.

**Core Outcome:** The player walks away from every interaction understanding *why* — the actual plan/principle behind a critical moment, grounded in engine truth — not a generic label, and sees their own recurring patterns emerge over time rather than re-discovering the same weakness game after game. Critically, this is a **two-way improvement loop**: the player's feedback on Jonathan's own analysis/diagnosis/exercises shapes how Jonathan approaches future sessions, so the coach itself gets better at coaching this specific player over time, not just a static tool.

**The Non-Negotiable:** The LLM never calculates chess itself — no legality checks, evaluations, or "best move" judgments come from the model's own reasoning. Every number and line comes from python-chess + local Stockfish; the LLM's only job is narrating that engine output into coaching language, and that narration must never contradict the engine's actual eval delta for a move.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| **Game Fetch** | Pulls the player's own games from chess.com under explicit user control (never a blind full sync) | A date-range spec: "this month," a specific month (e.g. May 2026), or a single day (21-05-2026); chess.com username (from profile) | New entries appended to `game-log.md`; underlying PGNs cached locally for analysis |
| **Game Analysis** | Deep, engine-grounded analysis of one game — 3-5 turning points, never ABC-level, reasoning tied to actual eval deltas. Two delivery modes: (a) interactive replay — visual board w/ forward/backward navigation + eval graph, player explains their own intent move-by-move, coach checks it against engine truth; (b) deep written report for later reading. Input source is source-agnostic: a fetched game, a pasted/uploaded PGN, or a legendary-game DB selection. | A game reference (game-log entry, raw PGN paste, or legendary-game selection) + optionally the player's stated plan/intent during replay | An interactive board+eval-graph artifact and/or a deep written per-turning-point report; `game-log.md` updated with analysis status + report link; candidate one-off patterns surfaced to `weaknesses.md` pending confirmation |
| **Weakness Diagnosis** | Mines a batch of the player's analyzed games for emergent, recurring patterns/"configurations" — no fixed taxonomy, whatever actually shows up (pawn structures, piece setups, tactical motifs, phase-specific struggles) | A batch spec (e.g. "diagnose my last 20 games," a date range) pulled from `game-log.md` | Updates `weaknesses.md`; a summary report (**good HTML dashboard candidate**: recurring issues ranked by frequency, linked example games/positions) |
| **Opening Repertoire Work** | Builds and reviews the player's opening repertoire — lines, sidelines, rationale | Player's questions/requests about a specific opening or line; existing `repertoire.md` content | Updates `repertoire.md`; repertoire notes/line trees |
| **Targeted Exercises** | Generates drills sourced from the player's *own* mistakes — positions right after a real critical moment, asking the player to find the engine-approved move/plan, graded against engine truth | A specific game's mistakes, or the curated `weaknesses.md` library | A set of custom exercises (reuses the board artifact from Game Analysis where useful) |
| **Flexible Training Plan** | A self-paced plan that adapts to irregular availability — no calendar/weekly assumption. Checks in on what was actually done and adjusts rather than issuing a fixed weekly schedule | Current `weaknesses.md` + `repertoire.md` state; player's stated available time/sessions; prior plan completion status | Updates `training-plan.md`; a plan of recommended next focus areas/exercises |
| **Tournament Prep** | Prep against a specific upcoming opponent — pulls their public games, surfaces their repertoire tendencies and holes, cross-references against the player's own `repertoire.md` | Opponent's chess.com username (reuses Game Fetch internals) | A prep report (**good HTML comparison-report candidate**: opponent tendencies vs. player's repertoire, highlighted gaps to exploit) |
| **Coach Self-Calibration** | The two-way improvement loop: reviews accumulated player feedback across all other capabilities and distills it into calibration notes that reshape how Jonathan approaches future analysis, diagnosis, and exercises | Accumulated raw entries in `feedback.md`; optionally a direct player prompt ("here's what's been bugging me about your reports") | Updated calibration-notes section of `feedback.md`; a short "here's what I'm adjusting" reflection back to the player |

<!-- Legendary-game study and custom/ad-hoc PGN analysis are intentionally NOT separate capabilities — they're input-source variants of Game Analysis (confirmed by user). -->

**Memory:** See Memory Architecture / Memory Contract above (`index.md`, `profile.md`, `weaknesses.md`, `game-log.md`, `repertoire.md`, `training-plan.md`) — shared across all capabilities of this single agent.

**Init Responsibility:** On first run, welcome the player, confirm the memory scaffold exists (defensive — in case the agent is invoked before the setup flow completes), orient via `index.md`, and offer to do an initial game fetch to seed `game-log.md` if the player wants to start right away.

**Activation Modes:** Primarily interactive (coaching conversation, replay sessions are inherently interactive). Game Fetch, Weakness Diagnosis, and single-game analysis in report mode can run headless/non-interactively (e.g. "pull my May 2026 games and diagnose patterns" end-to-end).

**Tool Dependencies:**
- Python + `python-chess` — PGN/FEN parsing, move legality, game-tree navigation
- Local Stockfish binary via UCI protocol (through `python-chess`'s engine integration) — positional evaluation and best-line generation
- chess.com public API — game fetch. Note: chess.com exposes **monthly** archives, not single-day queries — a single-day request means fetching that month's archive and filtering client-side. This is a non-obvious feasibility detail for the builder.

**Design Notes:**
- Hard rule (from the chess.com Game Review anti-pattern): narrative commentary must always be grounded in and consistent with the actual engine eval delta for that move — never an independent, possibly-contradicting impression.
- Must go past "ABC of chess" one-ply platitudes. In interactive mode, this is solved by having the *player* state their own multi-move intent, which the coach then checks against what the engine's principal variation actually shows — the LLM never invents the player's intention itself (that would violate the non-negotiable).
- Weakness diagnosis is deliberately emergent/open-ended, not a fixed checklist of categories (the player's own example — struggling against a queen-bishop battery — surfaced this way; it's an example outcome, not a required category).
- Game Fetch's explicit date-range control (vs. blind full sync) is a trust feature the player asked for directly — don't design around auto-syncing everything.
- The interactive-replay board and the deep written report may end up as one unified artifact (an HTML page that's both clickable/interactive AND contains the deep per-turning-point prose) rather than two separate deliverables — flagged as a build-time design option, not decided here.
- **Feedback collection is cross-cutting, not a standalone user-facing capability.** Every other capability's output should close with a lightweight invitation to rate/comment (logged as a raw entry in `feedback.md`); Coach Self-Calibration is the capability that actually reviews and distills those entries into behavior-shaping notes. Don't make the player manually "invoke feedback" after every single output — that would be friction that kills the habit.

**Relationships:** Game Fetch feeds Game Analysis, Weakness Diagnosis, and Tournament Prep. Weakness Diagnosis feeds Exercises and Training Plan (though Exercises can also draw directly from a single game's mistakes without going through the curated library). Opening Repertoire Work and Tournament Prep both read/write `repertoire.md`. Every capability feeds raw entries into `feedback.md`; Coach Self-Calibration reads that log and its distilled calibration notes are read back by every other capability on activation — the one deliberately cyclical relationship in the module. No hard ordering beyond natural data dependencies — can't diagnose before games are fetched/analyzed; can't build exercises from a library that doesn't exist yet (but can always build them from one fresh analyzed game).

---

## Configuration

Kept deliberately minimal — everything else is learned through conversation after setup and written into memory at that point (e.g., time-control preference, opening repertoire details).

| Variable | Prompt | Default | Result Template | User Setting |
| -------- | ------ | ------- | ---------------- | ------------ |
| `chess_com_username` | "What's your chess.com username?" | none (required) | seeds `profile.md` | yes |
| `current_rating` | "What's your current rating (and in what time control)?" | none | seeds `profile.md` | yes |
| `improvement_goals` | "What are you working on improving right now?" | none (open text) | seeds `profile.md` | yes |

## External Dependencies

- **Stockfish (local engine binary)** — required by every analysis capability for ground-truth evaluation and best lines. User does not have it installed and explicitly wants a friendly, guided install (not just "go install this yourself") since not every installer will be comfortable with it. Setup skill should: detect an existing install (check PATH / common install locations), and if missing, walk the user through OS-appropriate installation (download link / package manager command), then verify it runs and store the resolved binary path in config.
- **python-chess (Python package)** — needed by the module's own scripts for PGN/FEN parsing and move legality checks. Setup skill should check for a usable Python install and install the dependency (e.g., via a bundled `requirements.txt`), or guide the user if Python itself is missing.
- **chess.com public API** — used by the game-fetch capability to pull games by date range. No auth needed for public game archives; a build-time detail (not a setup-time dependency) but worth noting here for the builder.

## UI and Visualization

**Visual interactive board, chess.com-style** (forward/backward navigation), used during game-analysis/replay conversations alongside the chat — this is the centerpiece "delight" surface identified in brainstorming: it's what makes exploring candidate moves and strategy feel workable instead of exhausting to hold in your head.

Likely shape: an HTML artifact embedding a lightweight board renderer driven by the game's move list plus per-move engine eval, paired with an eval graph, regenerated per analysis/replay session. **Exact implementation is an open design question deferred to the build phase** (Agent Builder) — not resolved now, per the user's explicit "we can figure it out later."

## Setup Extensions

- Scaffold the bundled curated legendary-games PGN set into the module's data folder at install time (see External Dependencies / Skills for content: a small set — Fischer, Tal, Carlsen, etc.).
- Guide Stockfish detection/installation (see External Dependencies) and store the resolved binary path.
- Verify/install the `python-chess` dependency.
- Initialize the memory folder scaffold: seed `index.md` and `profile.md` from the three setup-time config answers; create the other curated memory files empty/with headers, populated as capabilities are first used.

## Integration

Not ready — complete in Phase 3+

## Creative Use Cases

Not ready — complete in Phase 3+

## Ideas Captured

- **Core idea:** a persistent Coach agent for an intermediate-to-strong club player (the user themself) that remembers profile (rating, opening repertoire, recurring weaknesses, goals) and guides improvement over time.
- **Hard constraint (non-negotiable):** the LLM must never calculate chess itself — no eyeballing positions, no "I think this move is better." All legality, evaluation, and best-line generation comes from python-chess (PGN/FEN parsing, move legality) + a local Stockfish engine. The LLM's job is strictly to turn engine output into human coaching language — explaining critical moments, principles, and patterns. This is the architectural spine of the whole module.
- **Candidate capabilities surfaced so far:**
  1. Game analysis from PGN — focus on 3-5 turning points rather than move-by-move dump
  2. Weakness diagnosis across a batch of games — pattern-finding over time, not just one game
  3. Opening repertoire work
  4. Targeted exercises built from the user's own mistakes (personalized tactics/puzzles sourced from their real games)
  5. Weekly training plan
- **MVP scope (user's own cut):** Coach agent + game analysis, with weakness diagnosis as a stretch-goal if feasible.
- **Game ingestion:** reach out to chess.com directly to pull games — but the user wants explicit control over the pull, not a blind "sync everything." Examples given: pull games for "this month," for "May 2026" specifically, or for a single day (21-05-2026). Implies a capability/tool with flexible date-range filtering, likely against chess.com's public monthly-archive API.
- **Delight factor:** the coach should proactively surface *specific recurring game configurations* the user struggles with — not just "you blundered tactically here" but patterns like a certain pawn structure, piece setup, or phase-of-game that keeps giving them trouble across many games. This is a sharper, more structural version of the weakness-diagnosis capability.
- **Reverse-brainstorm finding (critical anti-pattern to design against):** the worst version of this coach narrates moves without reasoning — "this move is bad" with no principle behind it. Every annotation must carry the *why*: the chess principle or pattern that explains the evaluation, not just the evaluation itself. This should probably become a hard design rule for the explanation-generation step across every analysis capability.
- **Beyond MVP — tournament prep:** prep against a specific upcoming opponent — pull their games (presumably also via chess.com), surface their repertoire tendencies and holes to exploit.
- **Beyond MVP — legendary games:** ability to load and analyze classic/master games, not just the user's own — same deep-analysis treatment applied to historical games for study purposes. Two sources: (a) a small curated database of famous games shipped with the module (Fischer, Tal, Carlsen, etc.), and (b) ad-hoc — user feeds in any arbitrary PGN (their own unplayed game, a friend's game, anything) for one-off analysis.
- **Pattern discovery is emergent, not pre-categorized:** the user explicitly does NOT want to pre-define categories of weakness (openings vs structures vs motifs). The coach should figure out whichever pattern actually shows up across the user's games — the user mentioned "I struggle against a queen-bishop battery" only as an example of the kind of thing that might surface, not as a required category. Diagnosis capability needs to be open-ended/exploratory across game data, not a fixed checklist.
- **Multi-user from day one:** the user is the first user, but the module must be installable by any club player — profile (chess.com username, rating, goals) is a setup-time/config concern, not hardcoded. This is a real product, not a one-off personal script.
- **Quality bar / north star (critical):** user has used chess.com's Game Review and was "quite disappointed" — explicitly states "if my coach stays at chess.com's Game Review level, I consider that a failure." This is the bar every capability must clear. Has not used Lichess analysis board, DecodeChess, or Aimchess.
- **Exactly what's wrong with chess.com Game Review (the anti-pattern spec):**
  1. Text comments are generic/superficial — stuck at "ABC of chess" level (e.g. "Good, you move the knight so it can control the center"). Never explains the deeper, multi-move intention — a 2-3 move prep, a lure, a plan — only the immediate textbook justification.
  2. Text commentary and the numeric move-score are sometimes **inconsistent/disconnected** — a very positive score paired with a negative-sounding comment or vice versa. This is a trust-breaker. Hard rule for cch: narrative commentary must always be grounded in and consistent with the actual engine eval delta for that move — never an independent, contradicting impression.
- **Why the LLM can't just "go deeper" by itself:** since the LLM must never calculate chess on its own, it can't just invent what the user's "real intention" was 3 moves ago — that would be exactly the kind of unfounded claim the non-negotiable forbids. The resolution: make game analysis conversational/interactive. The user replays the game WITH the coach and explains their own strategy/intent move by move; the coach's job is to take that stated intent and check it against engine ground truth (does the actual best line support that plan? did it work? where did it break down?) rather than guessing the intent itself.
- **Time controls:** user plays mainly 30-minute games and considers that the minimum for "a real game with real thought" vs. mechanical/memorized moves. Deprioritizes 10-minute-and-under games entirely. Implies: default filters/weighting for analysis and especially weakness-diagnosis should favor longer time controls; fast bullet/blitz games are lower-signal noise for pattern-finding.
- **Output format, two complementary modes:**
  1. **Interactive replay conversation** — replay the game together, visual board, user explains their strategy move by move, coach responds grounded in engine truth. This points toward a real visual/interactive artifact (board + eval graph), not just chat text.
  2. **Deep written report** — a per-move/critical-moment written analysis for later reading, not just live conversation.
- **Training plan needs to be flexible, not calendar-based:** user doesn't have guaranteed weekly play time. A fixed "weekly plan" assumption doesn't fit their real life — the plan needs to adapt to irregular/sparse availability rather than assuming a cadence.
- **Visual board confirmed, chess.com-style:** actual interactive board with forward/backward navigation buttons through the game, used alongside the conversation (not instead of it). User's own reasoning: trying to compare/explore different candidate moves purely in memory/imagination is exhausting — the visual board is what makes "let's try this move instead and see" actually workable during the coaching conversation. This is a real product surface, not a nice-to-have — likely an HTML artifact (board + move list + eval graph) that the agent drives alongside the chat.

## Build Roadmap

<!-- Recommended build order with rationale for why each skill should be built in that order -->

**Next steps:**

1. Build each skill using **Build an Agent (BA)** or **Build a Workflow (BW)** — share this plan document as context
2. When all skills are built, return to **Create Module (CM)** to scaffold the module infrastructure
