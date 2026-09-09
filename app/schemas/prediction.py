from pydantic import BaseModel, Field


class DemandPredictionRequest(BaseModel):

    target_month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Month to forecast, from 1 to 12"
    )


class DemandPredictionResponse(BaseModel):

    predicted_demand: float
    target_month: int
    unit: str
    historical_months_used: list[str]
    

class ShortageRiskRequest(BaseModel):

    target_month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Month for which shortage risk is estimated"
    )
    
class ShortageRiskResponse(BaseModel):

    predicted_demand: float
    current_inventory: float
    supply_gap: float
    shortage_probability: float
    risk_level: str