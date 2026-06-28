# Feature 1: Validation stubs

<!--
This worked example uses Python/pytest — illustrative only. Your own
features should use your project's test framework and language. Each stub
keeps its scenario ID (F1-S<n>) in the test name so the spec stays grep-able.
-->

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

<!-- Tech lead note: Approved 2026-05-13. Fixed RNG seed needed for F1-S1. Approved-by: @tech-lead -->

@pytest.fixture(autouse=True)
def fixed_seed():
    random.seed(42)
