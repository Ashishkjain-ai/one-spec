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
   `requirements.md`, 1:1, in this project's test framework and language.
   Flag any new dependencies/config needed.
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

## Enforcement

`spec-trace` is the linter for this convention. Run it to verify gate compliance,
coverage, and orphan IDs:

```bash
python spec-trace check
```

It exits 0 on all clear, 1 on any violation. The pre-commit hook
(`.one-spec/hooks/pre-commit`) and GitHub Action
(`.github/workflows/spec-trace.yml`) run it automatically. Wire up the hook once:

```bash
ln -s ../../.one-spec/hooks/pre-commit .git/hooks/pre-commit
```

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
