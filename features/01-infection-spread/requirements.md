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
