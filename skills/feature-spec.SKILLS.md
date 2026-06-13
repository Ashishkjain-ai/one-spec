# Skill: feature-spec

## Purpose

Draft a `requirements.md` file for a new feature, following the one-spec
convention, from a single one-line feature idea.

## Input

A one-line feature description from the user, e.g.:
> "Survivors should scavenge for supplies each tick"

## Before drafting

1. Check `roadmap.md` to determine the next feature number `<n>`.
2. Check existing `features/*/requirements.md` files to confirm the next
   scenario numbering starts at `S1` for this new feature (each feature's
   scenarios are numbered independently, starting from 1).
3. Create the folder `features/<NN>-<short-name>/` using a short kebab-case
   name derived from the feature idea.

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
