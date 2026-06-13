# one-spec — Project Context for Claude

## What this is

`one-spec` is a **zero-dependency markdown convention** (not a framework, not a CLI) for AI-agent-driven feature development. A single `requirements.md` file simultaneously serves as SDD scope, BDD Given/When/Then scenarios, and the source for TDD test stubs — unified by a grep-able scenario ID (`F<n>-S<n>`).

This repo *is* the product: it ships the convention definition, two Claude Code skills, and worked examples. Users copy it into their own repos.

---

## Repo structure

```
README.md                        # product pitch + quickstart
docs/ONE-SPEC.md                 # the convention spec itself
CLAUDE.md                        # ← this file
GAPS.md                          # active development plan (tracked items)
CLAUDE.md.additions.md           # snippet users paste into their own CLAUDE.md
features/
  _template/                     # blank templates (requirements/validation/plan)
  01-infection-spread/           # worked example — complete (all gates approved)
  02-supply-scavenging/          # worked example — mid-flow (awaiting product gate)
.claude/skills/
  feature-spec/SKILL.md          # drafts requirements.md from a one-liner
  one-spec-init/SKILL.md         # bootstraps the full convention into any repo
```

---

## What makes one-spec distinct (vs competitors)

Researched June 2026. Closest tools found:

| Tool | Overlap | Gap vs one-spec |
|---|---|---|
| GitHub Spec Kit | Gated phases, markdown artifacts, 29 agents | Separate spec/test files — no single-artifact SDD+BDD+TDD |
| AWS Kiro | Human approval gates, diff review | Full IDE, not a convention |
| LiorCohen/sdd | SPEC.md + PLAN.md + gates | Claude plugin (heavy), no traceability IDs, no BDD |
| leocamello/spec-kit-v-model | Traceability IDs, gate scripts, V-model | Requires Spec Kit, targets regulated industries (not our path) |
| shtracer | Grep-able `@REQ-001@` style IDs | Shell tool only, no BDD/TDD unification |

**One-spec's unique position:**
- Single artifact = SDD + BDD + TDD (no other tool does this)
- `F<n>-S<n>` IDs thread requirements → validation → plan → real test code
- Zero-dependency copy-paste (no install, works with any agent)
- Inline HTML comment governance (git-diffable, no external system)

---

## Decisions made

- **No regulatory / compliance angle.** Removed all SR 11-7, model-governance, and audit-trail language. one-spec targets everyday dev teams, not regulated industries (medical/automotive/aerospace space is leocamello/spec-kit-v-model's territory).
- **G3 governance path:** CODEOWNERS + `Approved-by:` git trailer backed by the linter — not the "honest-light" softening option.

---

## Active plan

See `ROADMAP.md` for the full tracked plan with statuses. Priority order:

1. **G1** — `spec-trace` linter (enforcement) — *the unlock for all other claims*
2. **G2** — Close the executable gap (validation.md IDs → real runnable tests)
3. **G3** — Credible governance (CODEOWNERS + linter check)
4. **G7** — Distribution hygiene (sync check for one-spec-init embed)
5. **G5** — README usability (end-to-end transcript, explain validation→tests)
6. **G4** — Team & lifecycle story ("Day 2")
7. **G6** — Naming/tagline polish

---

## Key files to keep in sync

`one-spec-init/SKILL.md` embeds verbatim copies of several files. When editing:
- `docs/ONE-SPEC.md` → also update its copy inside `one-spec-init/SKILL.md`
- `features/_template/*` → also update embedded copies in `one-spec-init/SKILL.md`
- `CLAUDE.md.additions.md` → also update embedded copy in `one-spec-init/SKILL.md`

G7 (sync check in CI) will eventually automate this catch.
