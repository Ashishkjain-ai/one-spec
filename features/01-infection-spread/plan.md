# Feature 1: Plan

## Components
- `Zone` class — holds infected/healthy counts, satisfies F1-S2, F1-S3
- `run_tick(zone, infection_rate)` — core spread logic, satisfies F1-S1

## Implementation order
1. Zone class + state representation (F1-S2, F1-S3 should pass trivially first)
2. run_tick infection logic (F1-S1)
3. Run validation.md suite, confirm all green
4. Update roadmap.md: mark Feature 1 complete
