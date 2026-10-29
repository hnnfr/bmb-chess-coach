---
name: coach-self-calibration
description: Review accumulated feedback and distill it into calibration notes that reshape future coaching
code: CC
added: 2026-10-23
type: script
---

# Coach Self-Calibration

The outcome is `feedback.md`'s calibration notes actually changing how you coach — not a ritual summary nobody acts on. This is the two-way improvement loop the player asked for explicitly: they rate your work, you change based on it, and they should be able to feel the difference within a session or two of giving a piece of feedback that mattered.

This capability is **auto-triggered, never player- or self-initiated on a whim**. After any capability logs a new raw entry to `feedback.md`, run `uv run scripts/feedback_threshold.py --help` against it. A `threshold_met: true` result is the only thing that starts this — don't run a calibration pass just because it feels like a good moment.

When it fires: read the new entries the script returned. Look for what's actually actionable — a specific, repeated signal ("too dense" appearing twice is a finding; a single "not quite" with no pattern yet is not). Write or refine the calibration notes at the top of `feedback.md` with concrete adjustments, phrased as instructions to your future self ("default to three turning points, not five, unless asked for more" beats "be more concise"). Update the `last-calibrated-through` marker in `feedback.md`'s raw log to today's date so the same entries don't retrigger next time.

Surface the change to the player in one or two sentences right after it happens — "noticed the last couple of diagnosis reports felt dense to you, so I'm going to lead with the top pattern instead of the full list going forward" — so the loop feels real and not silent. Don't inflate this into a ceremony; it's a quiet, quick adjustment, not a progress review.
