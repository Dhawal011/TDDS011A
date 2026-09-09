from app.services.prediction_service import (
    calculate_shortage_risk
)


def test_low_shortage_risk():

    result = calculate_shortage_risk(
        predicted_demand=300,
        current_inventory=400
    )

    assert result["risk_level"] == "LOW"
    assert result["supply_gap"] == 100


def test_medium_shortage_risk():

    result = calculate_shortage_risk(
        predicted_demand=400,
        current_inventory=320
    )

    assert result["risk_level"] == "MEDIUM"


def test_high_shortage_risk():

    result = calculate_shortage_risk(
        predicted_demand=400,
        current_inventory=200
    )

    assert result["risk_level"] == "HIGH"


def test_no_negative_shortage_probability():

    result = calculate_shortage_risk(
        predicted_demand=400,
        current_inventory=500
    )

    assert result["shortage_probability"] == 0