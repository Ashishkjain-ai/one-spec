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
├── CLAUDE.md                            # + workflow rules and role gates
├── spec-trace                           # linter — run: python spec-trace check
├── docs/
│   └── ONE-SPEC.md                      # the convention itself
├── .claude/skills/
│   ├── one-spec-init/SKILL.md           # one-time bootstrap skill (/one-spec-init)
│   └── feature-spec/SKILL.md            # drafts requirements.md from a one-liner (/feature-spec)
├── .github/workflows/
│   └── spec-trace.yml                   # CI: runs linter on every push and PR
├── .one-spec/hooks/
│   └── pre-commit                       # pre-commit hook (symlink once to .git/hooks/)
└── features/
    ├── _template/                       # blank templates to copy per feature
    │   ├── requirements.md              # SDD scope + BDD scenarios (Given/When/Then, tagged F<n>-S<n>)
    │   ├── validation.md                # TDD test stubs, 1:1 with scenario IDs
    │   └── plan.md                      # architecture, mapped to scenario IDs
    ├── 01-infection-spread/             # worked example: complete (both gates approved)
    │   ├── requirements.md
    │   ├── validation.md
    │   └── plan.md
    └── 02-supply-scavenging/            # worked example: mid-flow (awaiting product review)
        └── requirements.md              # only file present — gate not yet passed
```

No install. The skills live under `.claude/skills/` so Claude Code discovers
them as real, invokable skills. Copy the files in (or just drop in
`one-spec-init` and let it write the rest), add the CLAUDE.md additions, and
the convention is live on the next session.

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

No external approval system — the approval *is* a comment in the file Claude is about to act on next. Git-diffable and version-controlled alongside the spec itself.

## Enforcement (spec-trace)

`spec-trace` is a single-file Python linter (zero runtime dependencies) that gives the convention teeth. It runs four checks:

| Check | What it catches |
|---|---|
| **C4** Numbering | Feature folder NN prefixes not unique or contiguous |
| **C5** Gate state | `validation.md` or `plan.md` exists without the required approval comment |
| **C1** Coverage | Scenario ID in `requirements.md` with no matching stub in `validation.md` |
| **C2** Orphans | ID in `validation.md` or `plan.md` not defined in any `requirements.md` |
| **C3** Realization | Scenario with `plan.md` but no `test_F<n>_S<n>_*` function in any test file (requires `--repo-root`) |

```bash
python spec-trace check              # C4 + C5 + C1 + C2 — exits 0 on all clear
python spec-trace check --repo-root .  # also runs C3 (full check including real tests)
```

Ships with a GitHub Action (`.github/workflows/spec-trace.yml`) and a pre-commit hook (`.one-spec/hooks/pre-commit`). Wire up the hook once:

```bash
ln -s ../../.one-spec/hooks/pre-commit .git/hooks/pre-commit
```

## How it works (workflow)

1. Give Claude a one-line feature idea
2. `feature-spec` skill drafts `requirements.md` — SDD scope + BDD scenarios, each tagged `F<n>-S<n>`
3. **STOP** — product reviewer approves (inline comment in `requirements.md`)
4. Claude drafts `validation.md` — TDD test stubs, 1:1 with each scenario ID
5. **STOP** — tech lead approves (inline comment in `validation.md`)
6. Claude drafts `plan.md` — architecture, each component mapped to scenario IDs
7. Implementation proceeds: write real tests named `test_F<n>_S<n>_<description>()`, then make them green
8. On all-green: `python spec-trace check --repo-root .` confirms full coverage; update `roadmap.md`

## What it isn't

- Not a replacement for Spec Kit, OpenSpec, or Kiro — `one-spec`'s ID convention can be layered *into* an existing Spec Kit `specs/` folder
- Not a CLI (v1) — pure markdown convention, zero dependencies
- Not required to use `spec-trace` — the convention works without it; the linter is the optional enforcement layer that turns "by convention" into "by tooling"

## Quickstart

1. Copy `.claude/skills/one-spec-init/SKILL.md` into your project at the same
   path (`.claude/skills/one-spec-init/SKILL.md`)
2. Ask Claude: "set up one-spec here" (or run `/one-spec-init`)
3. Claude creates:
   - `docs/ONE-SPEC.md` — the convention reference
   - `.claude/skills/feature-spec/SKILL.md` — the drafting skill
   - `features/_template/*` — blank templates
   - `spec-trace` — the linter (copy this file, it has no dependencies)
   - `.github/workflows/spec-trace.yml` — CI enforcement
   - `.one-spec/hooks/pre-commit` — pre-commit hook
   - Updates your `CLAUDE.md` with the workflow rules
4. Wire up the pre-commit hook (one-time):
   ```bash
   ln -s ../../.one-spec/hooks/pre-commit .git/hooks/pre-commit
   ```
5. Verify everything is clean:
   ```bash
   python spec-trace check
   ```
6. Give Claude a one-line feature idea — the `feature-spec` skill takes it from there

> **Without `one-spec-init`:** copy `spec-trace` directly from this repo into
> your project root and run `python spec-trace check`. That's all it needs.

## License

MIT — see [LICENSE](LICENSE.txt)
