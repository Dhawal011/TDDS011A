from pydantic import BaseModel, Field

from app.schemas.donor import BloodGroup
from app.schemas.blood_request import BloodComponent


class InventoryCreate(BaseModel):

    blood_group: BloodGroup

    blood_component: BloodComponent

    units_available: int = Field(
        ...,
        ge=0,
        le=10000
    )


class InventoryResponse(BaseModel):

    id: int
    blood_group: str
    blood_component: str
    units_available: int

    class Config:
        from_attributes = True