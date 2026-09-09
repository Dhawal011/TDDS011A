from fastapi import APIRouter, HTTPException

from app.schemas.prediction import (
    DemandPredictionRequest,
    DemandPredictionResponse,
    ShortageRiskRequest,
    ShortageRiskResponse
)

from app.services.prediction_service import (
    predict_next_demand,
    calculate_shortage_risk,
    get_total_inventory
)

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.services.prediction_service import (
    predict_next_demand,
    calculate_shortage_risk
)

import json
from pathlib import Path


router = APIRouter(
    prefix="/prediction",
    tags=["ML Prediction"]
)


@router.post(
    "/demand",
    response_model=DemandPredictionResponse
)
def predict_blood_demand(
    request: DemandPredictionRequest
):

    try:

        result = predict_next_demand(
            target_month=request.target_month
        )

        return {
            "predicted_demand": result["predicted_demand"],
            "target_month": request.target_month,
            "unit": "blood units",
            "historical_months_used": (
                result["historical_months_used"]
            )
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.post(
    "/shortage-risk",
    response_model=ShortageRiskResponse
)
def predict_shortage_risk(
    request: ShortageRiskRequest,
    db: Session = Depends(get_db)
):

    try:

        demand_result = predict_next_demand(
            target_month=request.target_month
        )

        predicted_demand = (
            demand_result["predicted_demand"]
        )

        current_inventory = get_total_inventory(
            db
        )

        risk_result = calculate_shortage_risk(
            predicted_demand=predicted_demand,
            current_inventory=current_inventory
        )

        return {
            "predicted_demand": predicted_demand,
            "current_inventory": current_inventory,
            "supply_gap": risk_result["supply_gap"],
            "shortage_probability": (
                risk_result["shortage_probability"]
            ),
            "risk_level": risk_result["risk_level"]
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.get("/model-info")
def get_model_info():

    metadata_path = (
        Path(__file__).resolve().parent.parent
        / "ml"
        / "models"
        / "model_metadata.json"
    )

    if not metadata_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Model metadata not found"
        )

    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)