def get_outcome(angle_deg, probs, outcomes):
    """
    Returns the outcome (e.g., +200 or -200) based on angle (in degrees),
    lottery probabilities, and matching outcomes.
    """
    start_angle = 90  # lottery starts drawing at 90°
    for prob, outcome in zip(probs, outcomes):
        slice_size = prob * 360
        end_angle = (start_angle + slice_size) % 360

        if start_angle < end_angle:
            if start_angle <= angle_deg < end_angle:
                return outcome
        else:  # handle wrap-around (e.g., 350°–10°)
            if angle_deg >= start_angle or angle_deg < end_angle:
                return outcome

        start_angle = end_angle

    raise ValueError("Angle did not map to any outcome.")
