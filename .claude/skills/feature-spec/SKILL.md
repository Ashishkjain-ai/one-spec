---
name: feature-spec
description: Draft a one-spec requirements.md (SDD scope + BDD Given/When/Then scenarios, tagged F<n>-S<n>) for a new feature from a one-line idea. Use when the user gives a feature idea and the repo follows the one-spec convention. Stops after requirements.md — does not write validation.md or plan.md.
---

# Skill: feature-spec

## Purpose

Draft a `requirements.md` file for a new feature, following the one-spec
convention, from a single one-line feature idea.

## Input

A one-line feature description from the user, e.g.:
> "Survivors should scavenge for supplies each tick"

## Before drafting

1. Determine the next feature number `<n>`: take the highest `NN` prefix
   among existing `features/<NN>-*/` folders and add 1 (start at 1 if there
   are none). If a `roadmap.md` exists, cross-check the number against it —
   the `features/` directory is the source of truth, `roadmap.md` is a
   secondary check.
2. Each feature's scenarios are numbered independently, starting from `S1`.
3. Create the folder `features/<NN>-<short-name>/` using a short kebab-case
   name derived from the feature idea (zero-pad the number, e.g. `01`, `02`).

## Output: `requirements.md`

Produce a file with this structure:

```markdown
# Feature <n>: <Title>

<One paragraph: what this feature does and why, derived from the one-line idea.
Behavior only — no implementation detail, no library/class names.>

## Scenarios

### F<n>-S1
Given <initial state>
When <action/event>
Then <expected outcome>

### F<n>-S2
Given <initial state>
When <action/event>
Then <expected outcome>

<!-- continue for 2-5 scenarios total -->
```

## Rules

- **2 to 5 scenarios** per feature. Fewer than 2 suggests the feature is too
  trivial to need a spec; more than 5 suggests it should be split into
  multiple features.
- Always include at least one **edge case** scenario (empty/zero state,
  boundary condition, or error path) — not just the happy path.
- Scenario IDs are sequential and never reused, even if a scenario is later
  removed (leave a gap rather than renumber).
- Write scenarios in plain business language. A non-technical reviewer must
  be able to read and approve them without seeing code.
- Do NOT draft `validation.md` or `plan.md` in this step. Stop after
  `requirements.md` is written.

## After drafting

Output a short message to the user:

> Drafted `features/<NN>-<short-name>/requirements.md` with scenarios
> F<n>-S1 through F<n>-S<last>. This needs product reviewer approval
> (inline comment) before validation.md can be drafted.

Do not proceed to validation.md until an approval comment is present in
requirements.md (per CLAUDE.md workflow rules).
