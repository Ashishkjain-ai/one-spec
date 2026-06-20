# one-spec: Active Development Plan

Status key: `[ ]` not started · `[~]` in progress · `[x]` done

Priority order: G1 → G2 → G3 → G7 → G5 → G4 → G6

---

## Needle-movers

### [~] G1. `spec-trace` linter — give the convention teeth

**Problem.** Every value claim (traceability, gates, "living spec") rests on
an LLM voluntarily following `CLAUDE.md` prose. Nothing *fails* when the
convention is violated, so it will drift within weeks of real use.

**What to build — `spec-trace check` (single script, zero runtime deps):**
- Every `F<n>-S<n>` in `requirements.md` has a matching stub in
  `validation.md` (else: **untested requirement**)
- Every scenario ID in `validation.md` / `plan.md` exists in some
  `requirements.md` (else: **orphan / scope creep**)
- Every `F<n>-S<n>` resolves to at least one real test in the codebase
  (grep test files for the ID in name/comment) (else: **spec not realized**)
- Feature folder numbering is contiguous and unique
- Gate state is consistent (approval comment present before next file exists)

**Done when:** runs as `spec-trace check`, exits non-zero on violation,
ships a GitHub Action and a pre-commit hook.

**Effort:** M. **Unblocks:** every other claim in the README.

---

### [ ] G2. Close the executable gap — validation.md IDs → real tests

**Problem.** `validation.md` is pseudocode. The real red→green loop happens
in test files the convention doesn't track. "Failing test = spec diverged"
is not actually true — `validation.md` never runs.

**What to build:**
- Define the contract: each `F<n>-S<n>` MUST appear in a real test's
  name/docstring/tag (`test_F1_S1_infection_spreads`, `@pytest.mark.F1_S1`, etc.)
- Reframe `validation.md` explicitly as *acceptance criteria the tech lead
  approves*, not a stand-in for the test suite
- Update the worked example (Feature 1) to wire the stub to a runnable test
- G1's linter verifies the ID reached a runnable test

**Done when:** framework-agnostic rule is documented + Feature 1 worked
example has a real runnable test with the scenario ID in it.

**Effort:** S–M. **Unblocks:** the "living spec" claim.

---

### [ ] G3. Make approval credible — CODEOWNERS + linter check

**Problem.** Approval = anyone typing "Approved" in an HTML comment.
No identity, nothing that fails if skipped.

**What to build:**
- `CODEOWNERS` on `requirements.md` / `validation.md` — named reviewer must
  approve the PR that adds the approval comment
- OR: `Approved-by: <name>` git trailer that the linter checks against an
  allowlist
- G1's linter validates gate state (approval present before next artifact)

**Done when:** the gate cannot be bypassed without a named person's sign-off
that appears in git history.

**Effort:** M. **Unblocks:** trust that gates were actually enforced.

---

## Secondary

### [ ] G7. Distribution hygiene — sync check for one-spec-init embed

**Problem.** `one-spec-init/SKILL.md` embeds verbatim copies of every shipped
file. Edits must touch both source and embed or they silently drift.

**What to build:** a CI diff check (or build-time generation) that fails if
the embedded copies in `one-spec-init/SKILL.md` diverge from source files.

**Done when:** CI catches embed drift automatically.

**Effort:** S.

---

### [ ] G5. README usability — end-to-end transcript + explain the hard step

**What to add:**
- A real end-to-end transcript: one-line idea → `requirements.md` → gate →
  `validation.md` → runnable tests → green → roadmap update (show actual commands)
- Explain the operationally hardest step: how `validation.md` IDs reach real
  test code (don't hand-wave it)
- Document what `mission.md` / `tech-stack.md` / `roadmap.md` should contain
- Qualify strong claims ("living spec") with what's actually enforced vs. by convention

**Effort:** S–M.

---

### [ ] G4. Team & lifecycle story ("Day 2")

**What to add:** a "Working in a team" section covering:
- Multiple devs working on parallel features
- What happens when a scenario changes *after* code ships
- Deprecating a scenario ID
- Mapping features to issues/PRs
- `roadmap.md` merge conflicts

**Effort:** S.

---

### [ ] G6. Naming / tagline polish

**Problem.** "one-spec" reads as "a single spec file" — generic, collides
with OpenSpec / Spec Kit. The actual insight ("one artifact, three disciplines")
isn't in the name.

**Options:** rename to something that surfaces SDD+BDD+TDD unification, or
add a tagline that leads with the insight everywhere the name appears.

**Effort:** S (tagline) / M (rename + all references).

---

## What's already good (keep)

- `F<n>-S<n>` ID as a grep-able thread — genuinely useful, worth adopting standalone
- "One artifact, three lenses" framing — strong teaching anchor
- Worked examples cover both complete (F1) and mid-flow awaiting-gate (F2) states
- Zero-dependency copy-paste — clear differentiator vs GitHub Spec Kit / Kiro
