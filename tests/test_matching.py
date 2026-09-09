from app.services.matching_service import (
    get_compatible_donor_groups,
    calculate_distance_score,
    calculate_match_score
)


def test_o_positive_compatibility():

    groups = get_compatible_donor_groups("O+")

    assert "O+" in groups
    assert "O-" in groups
    assert "A+" not in groups
    assert "B+" not in groups


def test_ab_positive_compatibility():

    groups = get_compatible_donor_groups("AB+")

    assert len(groups) == 8


def test_distance_score():

    assert calculate_distance_score(2) == 100
    assert calculate_distance_score(5) == 90
    assert calculate_distance_score(10) == 75


def test_match_score():

    score = calculate_match_score(
        distance_km=2,
        urgency="CRITICAL"
    )

    assert score <= 100
    assert score > 90