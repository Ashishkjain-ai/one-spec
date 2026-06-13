# Skill: one-spec-init

## Purpose

Bootstrap the `one-spec` convention (SDD + BDD + TDD in one spec file) into
the current repository. This is a one-time setup skill — after running it,
this file can stay (as a re-init/update tool) or be removed.

## Trigger

User says something like "set up one-spec here", "initialize one-spec",
or "run one-spec-init".

## Flow

1. **Check current state** before writing anything:
   - Does `CLAUDE.md` exist at the repo root?
   - Do `docs/`, `skills/`, `features/` already exist?
   - Do `mission.md`, `tech-stack.md`, `roadmap.md` exist at the repo root?
     (one-spec does not create these — just note if missing)

2. **Create the following files** using the embedded content below.
   Do not overwrite files that already exist with the same path — if a
   conflict exists, tell the user and ask before overwriting.

   - `docs/ONE-SPEC.md`
   - `skills/feature-spec.SKILLS.md`
   - `features/_template/requirements.md`
   - `features/_template/validation.md`
   - `features/_template/plan.md`

3. **Update `CLAUDE.md`**:
   - If `CLAUDE.md` does not exist, create it with the content from the
     "CLAUDE.md additions" section below.
   - If `CLAUDE.md` already exists, append the "CLAUDE.md additions"
     section to the end of the file, under a `## one-spec` heading, rather
     than overwriting existing content.

4. **Report back to the user**:
   - List every file created (and any skipped due to conflicts)
   - Note any of `mission.md` / `tech-stack.md` / `roadmap.md` that are
     missing, with a one-line explanation that they're recommended but not
     required for one-spec itself
   - Offer: "Want me to draft the first feature spec? Give me a one-line
     idea and I'll use the feature-spec skill."

---

## Embedded files

The sections below contain the exact content to write to each path.
Everything between the opening and closing `~~~` fence for a given path
is the file content verbatim (including any nested ``` fences inside it).

### `docs/ONE-SPEC.md`

~~~markdown
# ONE-SPEC: The Convention

This document defines the `one-spec` convention — a small set of rules for
structuring feature specs so that a single `requirements.md` file serves as
SDD scope, BDD scenarios, and the source for TDD test stubs, with full
traceability from idea to roadmap.

There is no tooling required to follow this convention. It is a file format
and a workflow, expressed entirely in markdown.

---

## 1. The Scenario ID

Every behavioral scenario gets an ID: **`F<feature#>-S<scenario#>`**

- `F1-S1` = Feature 1, Scenario 1
- `F2-S3` = Feature 2, Scenario 3

This ID is the thread that runs through every file below. It is the only
piece of required structure — everything else is plain markdown.

---

## 2. File roles

Each feature lives in its own folder: `features/<NN>-<short-name>/`

### `requirements.md` — SDD + BDD

- A short paragraph of intent (SDD: what and why)
- A numbered list of Given/When/Then scenarios, each tagged with a scenario ID (BDD)
- No implementation detail — behavior only
- Reviewer approval recorded as an inline HTML comment

### `validation.md` — TDD

- One test stub per scenario ID, named or commented with that ID
- Written *before* implementation — these should fail initially
- Tech lead approval recorded as an inline HTML comment
- Any new dependencies or config needed are flagged here, *before* `plan.md`

### `plan.md` — Architecture

- Lists the components/modules needed
- Each component states which scenario IDs it satisfies
- Implementation order, ending with "run validation.md, confirm green, update roadmap.md"

---

## 3. Worked example: ZombieTracker Feature 1

**`features/01-infection-spread/requirements.md`**

```markdown
# Feature 1: Infection spread per tick

Each simulation tick, infected survivors may spread infection to healthy
survivors in the same zone, based on proximity and a configurable rate.

## Scenarios

### F1-S1
Given a zone with 3 infected and 7 healthy survivors
When a tick runs with infection rate 0.1
Then each healthy survivor has a 10% independent chance of becoming infected

### F1-S2
Given a zone with 0 infected survivors
When a tick runs
Then no healthy survivor becomes infected

### F1-S3
Given a zone with 10 infected and 0 healthy survivors
When a tick runs
Then the zone state remains unchanged (no division by zero, no errors)

<!-- Reviewer note (product reviewer): Approved 2026-05-12. -->
```

**`features/01-infection-spread/validation.md`**

```markdown
# Feature 1: Validation stubs

## F1-S1 → test_infection_spreads_probabilistically
def test_infection_spreads_probabilistically():
    zone = Zone(infected=3, healthy=7)
    run_tick(zone, infection_rate=0.1)
    assert approx_infection_rate(zone, trials=1000) == pytest.approx(0.1, abs=0.02)

## F1-S2 → test_no_infected_means_no_spread
def test_no_infected_means_no_spread():
    zone = Zone(infected=0, healthy=7)
    run_tick(zone, infection_rate=0.1)
    assert zone.infected == 0

## F1-S3 → test_no_healthy_survivors_no_error
def test_no_healthy_survivors_no_error():
    zone = Zone(infected=10, healthy=0)
    run_tick(zone, infection_rate=0.1)
    assert zone.healthy == 0

<!-- Tech lead note: Approved 2026-05-13. Fixed RNG seed needed for F1-S1. -->

@pytest.fixture(autouse=True)
def fixed_seed():
    random.seed(42)
```

**`features/01-infection-spread/plan.md`**

```markdown
# Feature 1: Plan

## Components
- `Zone` class — holds infected/healthy counts, satisfies F1-S2, F1-S3
- `run_tick(zone, infection_rate)` — core spread logic, satisfies F1-S1

## Implementation order
1. Zone class + state representation (F1-S2, F1-S3 should pass trivially first)
2. run_tick infection logic (F1-S1)
3. Run validation.md suite, confirm all green
4. Update roadmap.md: mark Feature 1 complete
```

---

## 4. The gate rule (governance)

Two stop points, enforced by your project's `CLAUDE.md`:

1. After `requirements.md` is drafted → **STOP**, wait for a product reviewer
   to add an approval comment before drafting `validation.md`
2. After `validation.md` is drafted → **STOP**, wait for a tech lead to add
   an approval comment before drafting `plan.md`

Approvals are HTML comments (`<!-- Reviewer note: ... -->`) inline in the
file. This means the approval is git-diffable, version-controlled, and sits
directly in the artifact the agent reads next — no external system needed.

---

## 5. Traceability

Because every scenario has an ID that appears in three files:

- To find what a requirement became as code: grep `F1-S1` across
  `validation.md` and `plan.md`
- To find what's untested: any scenario ID in `requirements.md` with no
  matching entry in `validation.md` is a gap
- To find scope creep: any test in `validation.md` with no corresponding
  scenario ID is undocumented behavior

This is the basis for an audit trail (e.g. SR 11-7 style traceability):
mission → requirement → scenario → test → code → roadmap, all connected by
plain-text IDs you can `grep`.

---

## 6. Compatibility

`one-spec`'s ID convention can be layered onto specs from other tools
(Spec Kit, OpenSpec, Kiro) by adding scenario IDs to their existing
requirements/spec files — it does not require replacing their structure.

~~~

### `skills/feature-spec.SKILLS.md`

~~~markdown
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

~~~

### `features/_template/requirements.md`

~~~markdown
# Feature <n>: <Title>

<!--
One paragraph: what this feature does and why.
Behavior only — no implementation detail, no library/class names.
-->

## Scenarios

### F<n>-S1
Given <initial state>
When <action/event>
Then <expected outcome>

### F<n>-S2
Given <initial state>
When <action/event>
Then <expected outcome>

<!--
- 2 to 5 scenarios total.
- Include at least one edge case (empty/zero/boundary/error).
- Scenario IDs are sequential, never reused.
-->

<!-- Reviewer note (product reviewer): -->

~~~

### `features/_template/validation.md`

~~~markdown
# Feature <n>: Validation stubs

<!--
One test stub per scenario ID from requirements.md, 1:1.
Written before implementation — these should fail initially.
Flag any new dependencies/config needed (before plan.md is drafted).
-->

## F<n>-S1 → test_<name>
def test_<name>():
    # arrange
    # act
    # assert
    pass

## F<n>-S2 → test_<name>
def test_<name>():
    # arrange
    # act
    # assert
    pass

<!-- Tech lead note: -->

~~~

### `features/_template/plan.md`

~~~markdown
# Feature <n>: Plan

## Components

- `<ComponentName>` — <what it does>, satisfies F<n>-S1, F<n>-S2
- `<ComponentName>` — <what it does>, satisfies F<n>-S...

## Implementation order

1. <step 1>
2. <step 2>
3. Run validation.md suite, confirm all green
4. Update roadmap.md: mark Feature <n> complete

~~~

### CLAUDE.md additions

~~~markdown
# CLAUDE.md additions for one-spec

Paste the section below into your project's `CLAUDE.md`. Adjust the
"Project" and "Stack" sections to match your repo — the "Workflow" and
"Roles" sections can be used as-is.

---

## Project
<!-- Replace with your project's mission/tech-stack/roadmap references -->
See `mission.md`, `tech-stack.md`, `roadmap.md` for project context.

## Stack
<!-- Replace with your actual stack -->
See `tech-stack.md`. Do not introduce new dependencies without updating
`tech-stack.md` first — flag this in `validation.md` if discovered during
test design.

## Roles
- **product reviewer**: approves `requirements.md` (inline comment) before
  `validation.md` is drafted
- **tech lead**: approves `validation.md` (inline comment) before `plan.md`
  is drafted

## Workflow (enforced — follow in order, do not skip steps)

1. New feature idea → invoke the `feature-spec` skill → drafts
   `features/<NN>-<name>/requirements.md` (SDD scope + BDD scenarios,
   tagged `F<n>-S<n>`)
2. **STOP.** Check `requirements.md` for a product reviewer approval
   comment. If absent, do not proceed — tell the user it's awaiting review.
3. Draft `validation.md` — one test stub per scenario ID from
   `requirements.md`, 1:1. Flag any new dependencies/config needed.
4. **STOP.** Check `validation.md` for a tech lead approval comment. If
   absent, do not proceed — tell the user it's awaiting review.
5. Draft `plan.md` — components mapped to the scenario IDs they satisfy,
   plus implementation order.
6. Implement against `validation.md`: red → green → refactor, one scenario
   ID at a time.
7. When all scenarios for the feature are green:
   - Update `roadmap.md` (mark feature complete)
   - Append a short summary to this file's context log (below), so future
     sessions know this feature exists and is done

## Context log
<!-- Claude appends one line per completed feature here -->
<!-- e.g.: Feature 1 (infection-spread) complete 2026-05-13, see features/01-infection-spread/ -->

---

## Notes on the gate checks

The approval comments look like this and live inline in the file:

```markdown
<!-- Reviewer note (product reviewer): Approved 2026-05-12. -->
```

```markdown
<!-- Tech lead note: Approved 2026-05-13. Fixed RNG seed needed for F1-S1. -->
```

Claude should look for these HTML comments specifically. If a human adds
notes *without* the word "Approved", treat it as feedback requiring changes
to `requirements.md`/`validation.md` before re-requesting approval — do not
treat any comment as automatic sign-off.

~~~

---

## Notes

- This skill is self-contained: a user only needs to copy this one file
  into `skills/one-spec-init.SKILLS.md` in their repo, then ask Claude to
  run it.
- After running, the repo has everything needed for the one-spec workflow:
  the convention doc, the feature-spec skill, empty templates, and updated
  CLAUDE.md workflow rules.
- Re-running this skill later (e.g. after a one-spec update) should follow
  the same conflict-checking logic in step 2 — never silently overwrite.