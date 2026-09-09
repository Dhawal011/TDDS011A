import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.inventory import BloodInventory


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml"
    / "models"
    / "blood_demand_model.joblib"
)

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "processed"
    / "blood_demand_clean.csv"
)


model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
FEATURES = model_package["features"]


def load_historical_data():

    df = pd.read_csv(DATA_PATH)

    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df.sort_values("DATE").reset_index(drop=True)

    return df


def predict_next_demand(target_month: int):

    df = load_historical_data()

    recent_demand = (
        df["QTY_DEMANDED"]
        .tail(6)
        .tolist()
    )

    if len(recent_demand) < 6:
        raise ValueError(
            "At least 6 months of historical demand are required."
        )

    lag_1 = recent_demand[-1]
    lag_2 = recent_demand[-2]
    lag_3 = recent_demand[-3]

    rolling_mean_3 = np.mean(
        recent_demand[-3:]
    )

    rolling_mean_6 = np.mean(
        recent_demand[-6:]
    )

    month_sin = np.sin(
        2 * np.pi * target_month / 12
    )

    month_cos = np.cos(
        2 * np.pi * target_month / 12
    )

    features = pd.DataFrame(
        [[
            lag_1,
            lag_2,
            lag_3,
            rolling_mean_3,
            rolling_mean_6,
            target_month,
            month_sin,
            month_cos
        ]],
        columns=FEATURES
    )

    prediction = model.predict(features)[0]

    return {
        "predicted_demand": max(
            0,
            round(float(prediction), 2)
        ),
        "historical_months_used": [
            str(date)
            for date in df["DATE"].tail(6)
        ]
    }
    
def calculate_shortage_risk(
    predicted_demand: float,
    current_inventory: float
):

    supply_gap = (
        current_inventory - predicted_demand
    )

    if predicted_demand <= 0:
        return {
            "supply_gap": round(supply_gap, 2),
            "shortage_probability": 0.0,
            "risk_level": "LOW"
        }

    shortage_ratio = (
        max(0, predicted_demand - current_inventory)
        / predicted_demand
    )

    shortage_probability = min(
        1.0,
        shortage_ratio
    )

    if current_inventory >= predicted_demand:
        risk_level = "LOW"

    elif current_inventory >= predicted_demand * 0.75:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    return {
        "supply_gap": round(supply_gap, 2),
        "shortage_probability": round(
            float(shortage_probability),
            2
        ),
        "risk_level": risk_level
    }
    
def get_total_inventory(db: Session):

    inventory_records = db.query(
        BloodInventory
    ).all()

    total_units = sum(
        item.units_available
        for item in inventory_records
    )

    return total_units