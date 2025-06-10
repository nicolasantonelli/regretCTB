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
