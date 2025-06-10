import pytest

def get_outcome(angle_deg, probs, outcomes):
    start_angle = 90
    for prob, outcome in zip(probs, outcomes):
        slice_size = prob * 360
        end_angle = (start_angle + slice_size) % 360

        if start_angle < end_angle:
            if start_angle <= angle_deg < end_angle:
                return outcome
        else:
            if angle_deg >= start_angle or angle_deg < end_angle:
                return outcome

        start_angle = end_angle

    raise ValueError("Angle did not map to any outcome.")


@pytest.mark.parametrize("angle,outcome", [
    (90,   200),
    (179,  200),
    (269, 200),
    (359, -200),
])
def test_get_outcome_simple_equal_split(angle, outcome):
    probs = [0.5, 0.5]
    outcomes = [200, -200]
    assert get_outcome(angle, probs, outcomes) == outcome

@pytest.mark.parametrize("angle,outcome", [
    (270, -200),  # exactly at start of second slice
    (0,   -200),  # well inside second slice
    (89,  -200),  # just before first slice
])
def test_get_outcome_edges(angle, outcome):
    probs = [0.5, 0.5]
    outcomes = [200, -200]
    assert get_outcome(angle, probs, outcomes) == outcome
def test_wraparound_slice():
    probs = [0.25, 0.75]
    outcomes = [999, -999]

    # Slice 1: 90° → 180°  = 25%
    # Slice 2: 180° → 90° (wraps around)

    assert get_outcome(91,  probs, outcomes) == 999
    assert get_outcome(270, probs, outcomes) == -999
    assert get_outcome(10,  probs, outcomes) == -999