"""
Real runnable tests for Feature 1: Infection spread per tick.

This file is the realization of features/01-infection-spread/validation.md.
The scenario IDs in each function name (F1_S1, F1_S2, F1_S3) are what
spec-trace C3 verifies when run with --repo-root, confirming that every
approved scenario reached actual test code.

In a real project, Zone and run_tick would be imported from application code.
This file includes minimal implementations so the worked example is fully
self-contained and passes as-is.
"""
import random
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Minimal implementations (in your project, import from your application)
# ---------------------------------------------------------------------------

@dataclass
class Zone:
    infected: int
    healthy: int


def run_tick(zone: Zone, infection_rate: float) -> None:
    if zone.infected == 0 or zone.healthy == 0:
        return
    newly_infected = sum(
        1 for _ in range(zone.healthy) if random.random() < infection_rate
    )
    zone.infected += newly_infected
    zone.healthy -= newly_infected


# ---------------------------------------------------------------------------
# F1-S1: probabilistic spread at a configurable rate
# ---------------------------------------------------------------------------

def test_F1_S1_infection_spreads_probabilistically():
    """F1-S1: each healthy survivor has an independent infection_rate chance per tick."""
    total_newly_infected = 0
    trials = 5_000
    for i in range(trials):
        random.seed(i)
        zone = Zone(infected=3, healthy=7)
        run_tick(zone, infection_rate=0.1)
        total_newly_infected += zone.infected - 3
    avg = total_newly_infected / trials
    assert abs(avg - 0.7) < 0.05  # expected: 7 healthy * 0.1 rate = 0.7 per trial


# ---------------------------------------------------------------------------
# F1-S2: no spread when no infected survivors
# ---------------------------------------------------------------------------

def test_F1_S2_no_infected_means_no_spread():
    """F1-S2: with 0 infected, no healthy survivor becomes infected."""
    zone = Zone(infected=0, healthy=7)
    run_tick(zone, infection_rate=0.1)
    assert zone.infected == 0
    assert zone.healthy == 7


# ---------------------------------------------------------------------------
# F1-S3: no errors when no healthy survivors
# ---------------------------------------------------------------------------

def test_F1_S3_no_healthy_survivors_no_error():
    """F1-S3: with 0 healthy survivors, tick completes cleanly and zone is unchanged."""
    zone = Zone(infected=10, healthy=0)
    run_tick(zone, infection_rate=0.1)
    assert zone.healthy == 0
    assert zone.infected == 10
