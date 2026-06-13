# one-spec

**One spec file. Three disciplines. Zero dependencies.**

## What is this?

`one-spec` is a lightweight convention — not a framework, not a CLI, not a dependency — for structuring AI-agent-driven feature development so that a single `requirements.md` file simultaneously serves as:

- **SDD** (Spec-Driven Development): the scope and intent of a feature, the source of truth an agent works from
- **BDD** (Behavior-Driven Development): Given/When/Then scenarios that are the shared contract between business stakeholders and engineers
- **TDD** (Test-Driven Development): the basis for `validation.md` test stubs, written before implementation, red before green

Most SDD tooling treats these as separate concerns — separate files, separate phases, separate tools. `one-spec` treats them as **one artifact, three lenses**. The same Given/When/Then scenario *is* the requirement, *is* the test case, *is* the documentation.

## Why "one-spec"?

> SDD asks "what are we building and why?"
> BDD asks "how do we describe behavior so everyone agrees?"
> TDD asks "how do we know it's done right?"
>
> `one-spec` answers all three with the same sentence: *Given X, when Y, then Z.*

## What's in the box

```
your-repo/
├── CLAUDE.md                      # + workflow rules and role gates
├── docs/
│   └── ONE-SPEC.md                # the convention itself
├── skills/
│   └── feature-spec.SKILLS.md     # teaches Claude to draft requirements.md from a one-liner
└── features/
    └── _template/
        ├── requirements.md        # SDD scope + BDD scenarios (Given/When/Then, tagged F<n>-S<n>)
        ├── validation.md          # TDD test stubs, 1:1 with scenario IDs
        └── plan.md                # architecture, mapped to scenario IDs
```

Four files. No install. Copy them into your repo, add the CLAUDE.md additions, and Claude Code picks up the convention on its next session.

## The core idea

Every scenario gets an ID: `F<feature#>-S<scenario#>` (e.g. `F1-S1`).

That ID is the thread:
- It appears in `requirements.md` as a Given/When/Then scenario
- It appears in `validation.md` as a test function name/comment
- It appears in `plan.md` as "this component satisfies F1-S1, F1-S3"
- It can be grepped across the codebase to answer "where did this requirement go?"

This is what makes the spec **living** — not because it's kept up to date by discipline, but because the test suite *is* the spec, and a failing test means the spec and code have diverged.

## The governance layer

Two human gates, enforced by `CLAUDE.md`, recorded as inline comments in the files themselves:

1. **Product reviewer** approves `requirements.md` before `validation.md` is drafted
2. **Tech lead** approves `validation.md` before implementation begins

No external approval system — the approval *is* a comment in the file Claude is about to act on next. Git-diffable, audit-friendly, and the basis for any SR 11-7 / model governance traceability story.

## How it works (workflow)

1. Give Claude a one-line feature idea
2. `feature-spec` skill drafts `requirements.md` — SDD scope + BDD scenarios, each tagged `F<n>-S<n>`
3. **STOP** — product reviewer approves (inline comment in `requirements.md`)
4. Claude drafts `validation.md` — TDD test stubs, 1:1 with each scenario ID
5. **STOP** — tech lead approves (inline comment in `validation.md`)
6. Claude drafts `plan.md` — architecture, each component mapped to scenario IDs
7. Implementation proceeds: red → green → refactor against `validation.md`
8. On all-green: update `roadmap.md`, append summary to `CLAUDE.md` context log

## What it isn't

- Not a replacement for Spec Kit, OpenSpec, or Kiro — `one-spec`'s ID convention can be layered *into* an existing Spec Kit `specs/` folder
- Not a CLI (v1) — pure markdown convention, zero dependencies
- Not enforcement — that's what an optional future linter (`spec-trace`, v2) would check

## Quickstart

1. Copy `skills/one-spec-init.SKILLS.md` into your project's `skills/` folder
2. Ask Claude: "set up one-spec here" (or "run one-spec-init")
3. Claude creates `docs/ONE-SPEC.md`, `skills/feature-spec.SKILLS.md`,
   `features/_template/*`, and updates your `CLAUDE.md`
4. Give Claude a one-line feature idea — the `feature-spec` skill takes it from there

## License

MIT — see [LICENSE](LICENSE.txt)
