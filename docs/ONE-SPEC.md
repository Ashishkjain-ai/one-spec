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
- Use your project's own test framework and language — the worked example
  below happens to use Python/pytest, but that is illustrative only

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
