---
name: one-spec-init
description: Bootstrap the one-spec convention (SDD + BDD + TDD in one spec file) into the current repo. Use when the user says "set up one-spec here", "initialize one-spec", or "run one-spec-init". Creates docs/ONE-SPEC.md, the feature-spec skill, feature templates, and updates CLAUDE.md.
---

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
   - Do `docs/`, `.claude/skills/`, `features/` already exist?
   - Do `mission.md`, `tech-stack.md`, `roadmap.md` exist at the repo root?

2. **Create the following files** using the embedded content below.
   Do not overwrite files that already exist with the same path — if a
   conflict exists, tell the user and ask before overwriting.

   - `docs/ONE-SPEC.md`
   - `.claude/skills/feature-spec/SKILL.md`
   - `features/_template/requirements.md`
   - `features/_template/validation.md`
   - `features/_template/plan.md`
   - `spec-trace` (the linter — Python, zero deps)
   - `.github/CODEOWNERS` (role-based approval enforcement — fill in handles)
   - `.github/workflows/spec-trace.yml` (CI check)
   - `.one-spec/hooks/pre-commit` (pre-commit hook)

3. **Update `CLAUDE.md`**:
   - If `CLAUDE.md` does not exist, create it with the content from the
     "CLAUDE.md additions" section below.
   - If `CLAUDE.md` already exists, append the "CLAUDE.md additions"
     section to the end of the file, under a `## one-spec` heading, rather
     than overwriting existing content.

4. **Offer to scaffold the project context files** (`mission.md`,
   `tech-stack.md`, `roadmap.md`). The one-spec workflow references these:
   `feature-spec` cross-checks `roadmap.md`, and `CLAUDE.md` points to all
   three. They are recommended but not required. If any are missing, offer
   to create starter versions using the "project context starters" section
   below — do not create them without asking, and never overwrite existing
   ones.

5. **Report back to the user**:
   - List every file created (and any skipped due to conflicts)
   - Note any of `mission.md` / `tech-stack.md` / `roadmap.md` that are
     missing, with a one-line explanation that they're recommended but not
     required for one-spec itself
   - Remind the user to fill in `.github/CODEOWNERS` with real GitHub handles
     and enable "Require review from Code Owners" in branch protection settings
   - Tell the user to wire up the pre-commit hook (one-time step):
     ```bash
     ln -s ../../.one-spec/hooks/pre-commit .git/hooks/pre-commit
     ```
   - Tell the user to verify the linter passes on the current state:
     ```bash
     python spec-trace check --repo-root .
     ```
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

### `validation.md` — Acceptance criteria (TDD anchor)

- One test stub per scenario ID — the tech lead's sign-off on *what the tests must verify*
- Written *before* implementation; this is the spec, not the runnable test suite
- Tech lead approval recorded as an inline HTML comment
- Any new dependencies or config needed are flagged here, *before* `plan.md`
- Use your project's own test framework and language for stubs

**Test naming contract:** each stub maps to a real test function whose name contains
the scenario ID in underscore form: `test_F1_S1_<description>()`. The `spec-trace`
C3 check (with `--repo-root .`) verifies this link exists in the codebase.

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

Approvals are HTML comments inline in the file and must name the approver:

```markdown
<!-- Reviewer note (product reviewer): Approved 2026-05-12. Approved-by: @alice -->
```

```markdown
<!-- Tech lead note: Approved 2026-05-13. Approved-by: @bob -->
```

The `Approved-by: @name` field is required — `spec-trace` rejects an approval
comment that is missing it (gate violation).

**Two enforcement layers:**

- **`CODEOWNERS`** (`.github/CODEOWNERS`): GitHub blocks the PR that adds the
  approval comment from merging unless the named owner has reviewed it. Fill in
  real GitHub handles and enable "Require review from Code Owners" in branch
  protection. This is the identity layer — it prevents self-approval.
- **`spec-trace` C5**: validates that the `Approved-by: @name` field is present
  and non-empty. Catches cases where someone writes "Approved" with no name.

Together: the approval is traceable to a named person (in the file), verified
by GitHub (CODEOWNERS), and enforced by the linter (spec-trace).

---

## 5. Traceability

Because every scenario has an ID that appears in spec files and real test code:

- To find what a requirement became as code: grep `F1-S1` across
  `validation.md`, `plan.md`, and test files
- To find what's untested: any scenario ID in `requirements.md` with no
  matching entry in `validation.md` is a gap
- To find scope creep: any test in `validation.md` with no corresponding
  scenario ID is undocumented behavior
- To verify real tests exist: `python spec-trace check --repo-root .` runs C3,
  catching any scenario whose ID never appeared in a test function name

This gives you a full traceable thread:
mission → requirement → scenario → validation stub → real test → code → roadmap,
all connected by plain-text IDs you can `grep`.

---

## 6. Compatibility

`one-spec`'s ID convention can be layered onto specs from other tools
(Spec Kit, OpenSpec, Kiro) by adding scenario IDs to their existing
requirements/spec files — it does not require replacing their structure.
~~~

### `.claude/skills/feature-spec/SKILL.md`

~~~markdown
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

<!-- Reviewer note (product reviewer): Approved YYYY-MM-DD. Approved-by: @your-handle -->
~~~

### `features/_template/validation.md`

~~~markdown
# Feature <n>: Validation stubs

<!--
One test stub per scenario ID from requirements.md, 1:1.
This is the tech lead's sign-off on *what the tests must verify* — not the
runnable test file itself. Flag any new dependencies/config needed here,
before plan.md is drafted.

Use your project's own test framework and language for stubs.

Test naming contract: each stub corresponds to a real test function whose name
contains the scenario ID in underscore form, e.g. test_F<n>_S<n>_<description>().
spec-trace C3 (run with --repo-root .) verifies this link exists.
-->

## F<n>-S1 → test_F<n>_S1_<description>
<!-- Given <initial state> / When <action> / Then <expected outcome> -->
TODO: implement test for F<n>-S1 in the project's test framework

## F<n>-S2 → test_F<n>_S2_<description>
<!-- Given <initial state> / When <action> / Then <expected outcome> -->
TODO: implement test for F<n>-S2 in the project's test framework

<!-- Tech lead note: Approved YYYY-MM-DD. Approved-by: @your-handle -->
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

### `spec-trace`

~~~python
#!/usr/bin/env python3
"""spec-trace: lint one-spec feature folders for convention compliance.

Checks (all run on every invocation):
  C4  Folder numbering — NN prefixes are unique and contiguous from 01
  C5  Gate state      — validation.md/plan.md only exist after approval
  C1  Coverage        — every F<n>-S<n> in requirements.md has a stub in validation.md
  C2  Orphans         — every ID in validation.md/plan.md exists in some requirements.md
  C3  Realization     — every scenario with plan.md has a test_F<n>_S<n>_* function
                        (only runs when --repo-root is provided)

Usage:
  python spec-trace check
  python spec-trace check --features-dir path/to/features
  python spec-trace check --repo-root .        # also runs C3
"""

import argparse
import re
import sys
from pathlib import Path

# ### F1-S1 header (defines a scenario in requirements.md)
_ID_HEADER = re.compile(r'^###\s+(F\d+-S\d+)\s*$', re.MULTILINE)
# Any F1-S1 reference anywhere in a file
_ID_REF = re.compile(r'\bF\d+-S\d+\b')
# Individual HTML comments (matched one at a time to avoid cross-comment false positives)
_HTML_COMMENT = re.compile(r'<!--(.*?)-->', re.DOTALL)
# test_F1_S1_* function definition in a Python test file
_TEST_FN = re.compile(r'def\s+test_[A-Za-z0-9_]*F(\d+)_S(\d+)', re.MULTILINE)
# Approved-by: @name (or Approved-by: name) inside an approval comment
_APPROVED_BY = re.compile(r'approved-by:\s*\S', re.IGNORECASE)


def _read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def _defined_ids(requirements: Path) -> list:
    return _ID_HEADER.findall(_read(requirements))


def _referenced_ids(path: Path) -> set:
    return set(_ID_REF.findall(_read(path)))


def _approval_status(path: Path, role: str) -> str:
    """Check approval state of a file for the given role.

    Returns:
      'approved'      — comment has role + approved + Approved-by: <name>
      'missing-name'  — comment has role + approved but no Approved-by field
      'unapproved'    — no matching approval comment found
    """
    role_lower = role.lower()
    for m in _HTML_COMMENT.finditer(_read(path)):
        body = m.group(1)
        body_lower = body.lower()
        if role_lower in body_lower and 'approved' in body_lower:
            if _APPROVED_BY.search(body):
                return 'approved'
            return 'missing-name'
    return 'unapproved'


def _feature_folders(features_dir: Path) -> list:
    return sorted(
        d for d in features_dir.iterdir()
        if d.is_dir() and d.name != '_template'
    )


def _check_numbering(folders: list) -> list:
    failures = []
    prefixes = []
    for folder in folders:
        m = re.match(r'^(\d+)-', folder.name)
        if not m:
            failures.append(
                f"FAIL {folder.name}: folder name must start with a zero-padded "
                f"number followed by a dash (e.g. 01-my-feature)"
            )
            continue
        prefixes.append(int(m.group(1)))
    seen: set = set()
    for n in prefixes:
        if n in seen:
            failures.append(f"FAIL features/: duplicate folder number {n:02d}")
        seen.add(n)
    for i, n in enumerate(sorted(prefixes), start=1):
        if n != i:
            failures.append(
                f"FAIL features/: numbering gap — expected {i:02d}, found {n:02d}"
            )
            break
    return failures


def _check_gates(folders: list) -> list:
    failures = []
    for folder in folders:
        req  = folder / 'requirements.md'
        val  = folder / 'validation.md'
        plan = folder / 'plan.md'
        if val.exists():
            if not req.exists():
                failures.append(
                    f"FAIL {folder.name}: validation.md exists but requirements.md is missing"
                )
            else:
                status = _approval_status(req, 'reviewer note')
                if status == 'unapproved':
                    failures.append(
                        f"FAIL {folder.name}: gate 1 violated — validation.md exists but "
                        f"requirements.md has no approval comment"
                    )
                elif status == 'missing-name':
                    failures.append(
                        f"FAIL {folder.name}: gate 1 violated — requirements.md approval "
                        f"comment is missing 'Approved-by: @name'"
                    )
        if plan.exists():
            if not val.exists():
                failures.append(
                    f"FAIL {folder.name}: plan.md exists but validation.md is missing"
                )
            else:
                status = _approval_status(val, 'tech lead note')
                if status == 'unapproved':
                    failures.append(
                        f"FAIL {folder.name}: gate 2 violated — plan.md exists but "
                        f"validation.md has no approval comment"
                    )
                elif status == 'missing-name':
                    failures.append(
                        f"FAIL {folder.name}: gate 2 violated — validation.md approval "
                        f"comment is missing 'Approved-by: @name'"
                    )
    return failures


def _check_coverage(folders: list) -> list:
    failures = []
    for folder in folders:
        req = folder / 'requirements.md'
        val = folder / 'validation.md'
        if not req.exists() or not val.exists():
            continue
        referenced = _referenced_ids(val)
        for id_ in _defined_ids(req):
            if id_ not in referenced:
                failures.append(
                    f"FAIL {folder.name}: {id_} defined in requirements.md "
                    f"has no stub in validation.md"
                )
    return failures


def _check_orphans(folders: list) -> list:
    failures = []
    known: set = set()
    for folder in folders:
        req = folder / 'requirements.md'
        if req.exists():
            known.update(_defined_ids(req))
    for folder in folders:
        for filename in ('validation.md', 'plan.md'):
            path = folder / filename
            if not path.exists():
                continue
            for id_ in _referenced_ids(path):
                if id_ not in known:
                    failures.append(
                        f"FAIL {folder.name}/{filename}: {id_} not defined in any "
                        f"requirements.md (orphan ID — possible scope creep)"
                    )
    return failures


def _realized_ids(repo_root: Path) -> set:
    """IDs that appear in a test function name (test_F<n>_S<n>_*) under repo_root."""
    realized = set()
    seen: set = set()
    for pattern in ('test_*.py', '*_test.py'):
        for tf in repo_root.rglob(pattern):
            if tf in seen:
                continue
            seen.add(tf)
            for m in _TEST_FN.finditer(_read(tf)):
                realized.add(f'F{m.group(1)}-S{m.group(2)}')
    return realized


def _check_realization(folders: list, repo_root: Path) -> list:
    """C3: every scenario with plan.md must appear in a real test function name."""
    realized = _realized_ids(repo_root)
    failures = []
    for folder in folders:
        req  = folder / 'requirements.md'
        plan = folder / 'plan.md'
        if not req.exists() or not plan.exists():
            continue
        for id_ in _defined_ids(req):
            if id_ not in realized:
                norm = id_.replace('-', '_')
                failures.append(
                    f"FAIL {folder.name}: {id_} has no real test function "
                    f"(add a function named test_{norm}_* to a test file)"
                )
    return failures


def cmd_check(features_dir: Path, repo_root: Path = None) -> int:
    if not features_dir.exists():
        print(f"ERROR: features directory not found: {features_dir}", file=sys.stderr)
        return 1
    folders = _feature_folders(features_dir)
    failures = (
        _check_numbering(folders)
        + _check_gates(folders)
        + _check_coverage(folders)
        + _check_orphans(folders)
        + (_check_realization(folders, repo_root) if repo_root is not None else [])
    )
    if failures:
        for line in failures:
            print(line)
        print(f"\n{len(failures)} violation(s).")
        return 1
    scenario_count = sum(
        len(_defined_ids(f / 'requirements.md'))
        for f in folders
        if (f / 'requirements.md').exists()
    )
    print(f"PASS {len(folders)} feature(s), {scenario_count} scenario(s) — all clear.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='spec-trace',
        description='Lint one-spec feature folders for convention compliance.',
    )
    sub = parser.add_subparsers(dest='cmd')
    p = sub.add_parser('check', help='Run all checks (exits 1 on any violation)')
    p.add_argument(
        '--features-dir',
        default='features',
        metavar='DIR',
        help='Path to features directory (default: ./features)',
    )
    p.add_argument(
        '--repo-root',
        default=None,
        metavar='DIR',
        help='Repo root for C3 realization check — searches test_*.py files for '
             'scenario IDs in function names. If omitted, C3 is skipped.',
    )
    args = parser.parse_args()
    if args.cmd == 'check':
        sys.exit(cmd_check(
            Path(args.features_dir),
            repo_root=Path(args.repo_root) if args.repo_root else None,
        ))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
~~~

### `.github/CODEOWNERS`

~~~
# one-spec CODEOWNERS — enforces role-based approval at the PR level.
#
# GitHub blocks merging any PR that touches these files unless the named
# owner has approved it. This is the identity layer that backs the
# Approved-by: @name field in the approval comment.
#
# Replace the placeholders with real GitHub handles, then enable
# "Require review from Code Owners" in your branch protection rules.

# Gate 1: product reviewer must approve PRs that add/modify requirements.md
features/*/requirements.md   @REPLACE-WITH-PRODUCT-REVIEWER

# Gate 2: tech lead must approve PRs that add/modify validation.md
features/*/validation.md     @REPLACE-WITH-TECH-LEAD
~~~

### `.github/workflows/spec-trace.yml`

~~~yaml
name: spec-trace

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run spec-trace
        run: python spec-trace check --repo-root .
      - name: Run spec-trace tests
        run: python -m unittest discover -s tests -v
~~~

### `.one-spec/hooks/pre-commit`

~~~sh
#!/bin/sh
# spec-trace pre-commit hook — blocks commits that violate the one-spec convention.
# Wire it up once:
#   ln -s ../../.one-spec/hooks/pre-commit .git/hooks/pre-commit
python spec-trace check --repo-root .
~~~

### CLAUDE.md additions

~~~markdown
# CLAUDE.md additions for one-spec

Paste the section below into your project's `CLAUDE.md`. Adjust the
"Project" and "Stack" sections to match your repo — the "Workflow",
"Roles", and "Notes on the gate checks" sections can be used as-is.

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
   `requirements.md`, 1:1, in this project's test framework and language.
   Flag any new dependencies/config needed.
4. **STOP.** Check `validation.md` for a tech lead approval comment. If
   absent, do not proceed — tell the user it's awaiting review.
5. Draft `plan.md` — components mapped to the scenario IDs they satisfy,
   plus implementation order.
6. Implement: write real tests named `test_F<n>_S<n>_<description>()`, make them
   green against the implementation.
7. When all scenarios for the feature are green:
   - Run `python spec-trace check --repo-root .` to confirm full coverage (C3)
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
<!-- Reviewer note (product reviewer): Approved 2026-05-12. Approved-by: @alice -->
```

```markdown
<!-- Tech lead note: Approved 2026-05-13. Approved-by: @bob -->
```

The `Approved-by: @name` field is **required** — `spec-trace` rejects approval
comments that are missing it. Claude should check for both "Approved" and
"Approved-by: @name" before treating a gate as passed.

If a human adds notes *without* the word "Approved", treat it as feedback
requiring changes before re-requesting approval — do not treat any comment as
automatic sign-off.
~~~

---

## Project context starters

Only used in step 4, and only if the user agrees. These are optional —
one-spec works without them, but the workflow references them. Never
overwrite an existing file.

### `mission.md`

~~~markdown
# Mission

<!-- One or two paragraphs: what this project is for and who it serves. -->

## Goals
- <goal>

## Non-goals
- <explicitly out of scope>
~~~

### `tech-stack.md`

~~~markdown
# Tech Stack

<!-- The languages, frameworks, and key dependencies this project uses. -->
<!-- one-spec rule: do not add a new dependency without updating this file. -->

- Language:
- Test framework:
- Key dependencies:
~~~

### `roadmap.md`

~~~markdown
# Roadmap

<!-- One line per feature. feature-spec cross-checks the next number here. -->

| #  | Feature | Status |
|----|---------|--------|
| 01 | <name>  | planned |
~~~

---

## Notes

- This skill is self-contained: a user only needs to copy this one file
  into `.claude/skills/one-spec-init/SKILL.md` in their repo, then ask
  Claude to run it.
- After running, the repo has everything needed for the one-spec workflow:
  the convention doc, the feature-spec skill, empty templates, and updated
  CLAUDE.md workflow rules.
- Re-running this skill later (e.g. after a one-spec update) should follow
  the same conflict-checking logic in step 2 — never silently overwrite.
