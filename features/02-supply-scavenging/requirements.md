# Feature 2: Supply scavenging per tick

Each simulation tick, healthy survivors in a zone scavenge from the zone's
shared supply pool, picking up supplies up to a per-tick limit, so that
survivors can sustain themselves between infection events.

## Scenarios

### F2-S1
Given a zone with 100 supplies and 5 healthy survivors, each with a per-tick pickup limit of 3
When a tick runs
Then each survivor's inventory increases by up to 3 and the zone pool decreases by the total collected

### F2-S2
Given a zone with 0 supplies remaining
When a tick runs
Then no survivor's inventory changes and the pool stays at 0

### F2-S3
Given a zone with 4 supplies and 5 healthy survivors each wanting 3
When a tick runs
Then supplies are distributed until the pool is exhausted, the pool never goes negative, and survivors left unserved simply collect nothing

<!--
- This feature is drafted and AWAITING product reviewer approval.
- Note the empty reviewer comment below: no "Approved" means the workflow
  STOPs here — validation.md and plan.md are not drafted yet (that's why
  this folder has only requirements.md).
-->

<!-- Reviewer note (product reviewer): -->
