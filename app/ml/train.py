import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)


DATA_PATH = "data/processed/blood_demand_clean.csv"

MODEL_PATH = (
    "app/ml/models/blood_demand_model.joblib"
)

METADATA_PATH = (
    "app/ml/models/model_metadata.json"
)


FEATURES = [
    "LAG_1",
    "LAG_2",
    "LAG_3",
    "ROLLING_MEAN_3",
    "ROLLING_MEAN_6",
    "MONTH_NUMBER",
    "MONTH_SIN",
    "MONTH_COS"
]


def prepare_data():

    df = pd.read_csv(DATA_PATH)

    df["DATE"] = pd.to_datetime(df["DATE"])

    df = df.sort_values(
        "DATE"
    ).reset_index(drop=True)

    df["LAG_1"] = (
        df["QTY_DEMANDED"].shift(1)
    )

    df["LAG_2"] = (
        df["QTY_DEMANDED"].shift(2)
    )

    df["LAG_3"] = (
        df["QTY_DEMANDED"].shift(3)
    )

    df["ROLLING_MEAN_3"] = (
        df["QTY_DEMANDED"]
        .shift(1)
        .rolling(3)
        .mean()
    )

    df["ROLLING_MEAN_6"] = (
        df["QTY_DEMANDED"]
        .shift(1)
        .rolling(6)
        .mean()
    )

    df["MONTH_NUMBER"] = (
        df["DATE"].dt.month
    )

    df["MONTH_SIN"] = np.sin(
        2 * np.pi *
        df["MONTH_NUMBER"] / 12
    )

    df["MONTH_COS"] = np.cos(
        2 * np.pi *
        df["MONTH_NUMBER"] / 12
    )

    df = df.dropna().reset_index(
        drop=True
    )

    return df


def train_model():

    df = prepare_data()

    # -------------------------------
    # Time-based evaluation split
    # -------------------------------

    train = df[
        df["DATE"] < "2019-01-01"
    ].copy()

    test = df[
        df["DATE"] >= "2019-01-01"
    ].copy()

    X_train = train[FEATURES]
    y_train = train["QTY_DEMANDED"]

    X_test = test[FEATURES]
    y_test = test["QTY_DEMANDED"]

    evaluation_model = LinearRegression()

    evaluation_model.fit(
        X_train,
        y_train
    )

    predictions = evaluation_model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    mape = (
        mean_absolute_percentage_error(
            y_test,
            predictions
        ) * 100
    )

    # -------------------------------
    # Final production model
    # -------------------------------

    final_model = LinearRegression()

    final_model.fit(
        df[FEATURES],
        df["QTY_DEMANDED"]
    )

    model_package = {
        "model": final_model,
        "features": FEATURES
    }

    Path(MODEL_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model_package,
        MODEL_PATH
    )

    # -------------------------------
    # Save metadata
    # -------------------------------

    metadata = {
        "model_name": "Linear Regression",
        "problem": "Monthly Blood Demand Forecasting",
        "evaluation_period": (
            "2019-01-01 to 2020-09-01"
        ),
        "evaluation_training_samples": int(
            len(train)
        ),
        "evaluation_test_samples": int(
            len(test)
        ),
        "final_training_samples": int(
            len(df)
        ),
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "mape": round(float(mape), 2),
        "features": FEATURES
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    print(
        "Final model trained successfully."
    )

    print(
        f"Evaluation training samples: {len(train)}"
    )

    print(
        f"Evaluation test samples: {len(test)}"
    )

    print(
        f"Final training samples: {len(df)}"
    )

    print(
        f"MAE: {mae:.2f}"
    )

    print(
        f"RMSE: {rmse:.2f}"
    )

    print(
        f"MAPE: {mape:.2f}%"
    )

    print(
        f"Model saved to: {MODEL_PATH}"
    )

    print(
        f"Metadata saved to: {METADATA_PATH}"
    )


if __name__ == "__main__":
    train_model()