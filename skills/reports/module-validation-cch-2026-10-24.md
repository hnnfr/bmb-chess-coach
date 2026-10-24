# Module Validation Report — Chess Coach (`cch`)

**Date:** 2026-10-24
**Module:** Chess Coach (`cch`) — standalone, self-registering
**Skill:** `cch-agent-coach` (agent: Jonathan, `agent-coach`)

## Structural Validation (script)

**Status: PASS — 0 findings.**

- Standalone module correctly detected (no `-setup` skill; `assets/module.yaml` present directly in the skill).
- All required files present: `SKILL.md`, `assets/module.yaml`, `assets/module-help.csv`, `assets/module-setup.md`, `scripts/merge-config.py`, `scripts/merge-help-csv.py`.
- 9 CSV entries, all mapped to the single skill folder (`cch-agent-coach`), no orphans, no duplicate menu codes, no broken `preceded-by`/`followed-by` references.
- `module.yaml` required fields (`code`, `name`, `description`) all present.

**Tooling note (informational, not a module defect):** `validate-module.py`'s own `parse_yaml_minimal()` is a deliberately flat, non-nested YAML scanner. Because `module.yaml`'s `agents:` list entries carry their own `name`/`description` fields, the scanner's flat line-scan overwrites the top-level module `name`/`description` with the *agent's* values when building its `info` display block — it reported `module_name: "Jonathan"` instead of `"Chess Coach"`. Verified independently with a real YAML parser (PyYAML) that the actual file content is correct: top-level `name: "Chess Coach"` is untouched. This does not produce a false finding (the script's actual check is field *presence*, not value correctness) and is a limitation in `bmad-module-builder`'s own shared script, not in this module — likely affects the `info` display for any module with an `agents:` roster. Out of scope to fix here.

## Quality Assessment

- **Completeness:** ✓ All 8 capabilities (`GF`, `GA`, `WD`, `OR`, `EX`, `TP`, `VP`, `CC`) registered, one row each, plus `SU` for setup/configure.
- **Accuracy:** ✓ Every CSV `action` matches its capability file's frontmatter `name:` field exactly.
- **Agent roster:** ✓ `module.yaml`'s `agents:` entry matches `cch-agent-coach/customize.toml`'s `[agent]` block field-for-field (`code`, `name`, `title`, `icon`, `description`). No drift.
- **Description quality:** found and fixed — 4 descriptions were not verb-first:

  | Code | Before | After |
  |---|---|---|
  | GA | "Deep engine-grounded analysis of one game's turning points" | "Analyze a game's turning points grounded in actual engine evaluations" |
  | EX | "Drills sourced from the player's own mistakes" | "Generate drills sourced from the player's own mistakes" |
  | TP (was FT) | "Flexible self-paced training plan with no calendar assumption" | "Maintain a flexible self-paced training plan with no calendar assumption" |
  | CC | "Auto-triggered review of accumulated feedback (not user-invoked)" | "Review accumulated feedback and recalibrate the coaching approach (auto-triggered not user-invoked)" |

- **Menu codes:** found and fixed — `FT` for "Training Plan" didn't map intuitively to the display name. Renamed to `TP` in both `assets/module-help.csv` and `references/training-plan.md`'s frontmatter `code:` field, keeping the auto-generated `CAPABILITIES.md` registry and the help CSV in agreement. Verified via a fresh `init-sanctum.py` run: `CAPABILITIES.md` now shows `[TP] training-plan` correctly.
- **Ordering:** ✓ `preceded-by`/`followed-by` chain (GF→GA→WD→TP, GA→EX) matches the capabilities' actual data dependencies. `required` correctly `false` throughout — consistent with a conversational agent rather than a rigid gated workflow.

## Separately Noted (from the Create Module step, carried forward for visibility)

- A real path bug was found and fixed in this module's copy of `assets/module-setup.md` (inherited from `bmad-module-builder`'s own shared `standalone-module-template`): it referenced `./assets/module.yaml` and `./scripts/merge-config.py` as if the file lived at the skill root, but it actually gets placed inside `assets/` — making those references resolve to nonexistent nested paths. Fixed here; the upstream shared template was not touched (different skill's maintenance boundary) and likely has the same latent bug for every other standalone module scaffolded by this tool.
- `skills/.claude-plugin/marketplace.json` has blank `owner`/`license`/`homepage`/`repository` fields — intentionally left for the module owner to fill before distribution.

## Overall Assessment

**Ready for use.** All structural checks pass. The quality findings identified above (description wording, one menu-code rename) have been applied and re-verified. No outstanding issues block installation or use of the Chess Coach module.

**Validation complete.**
