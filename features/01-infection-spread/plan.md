# Feature 1: Plan

## Components
- `Zone` class — holds infected/healthy counts, satisfies F1-S2, F1-S3
- `run_tick(zone, infection_rate)` — core spread logic, satisfies F1-S1

## Implementation order
1. Zone class + state representation (F1-S2, F1-S3 should pass trivially first)
2. run_tick infection logic (F1-S1)
3. Write real tests in `tests/test_infection_spread.py` with IDs in function names
   (test_F1_S1_*, test_F1_S2_*, test_F1_S3_*) — red first, then green
4. Run `python spec-trace check --repo-root .` — confirm all clear including C3
5. Update roadmap.md: mark Feature 1 complete
