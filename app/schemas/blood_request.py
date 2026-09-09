from enum import Enum

from pydantic import BaseModel, Field, field_validator

from app.schemas.donor import BloodGroup


class BloodComponent(str, Enum):
    WHOLE_BLOOD = "WHOLE BLOOD"
    PACKED_RBC = "PACKED RBC"
    PLASMA = "PLASMA"
    PLATELETS = "PLATELETS"


class Urgency(str, Enum):
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BloodRequestCreate(BaseModel):

    hospital_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    blood_group: BloodGroup

    blood_component: BloodComponent

    units_required: int = Field(
        ...,
        gt=0,
        le=20
    )

    urgency: Urgency

    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    latitude: float | None = None

    longitude: float | None = None

    @field_validator("blood_group", mode="before")
    @classmethod
    def normalize_blood_group(cls, value):
        return value.upper()


class BloodRequestResponse(BaseModel):

    id: int

    hospital_name: str

    blood_group: str

    blood_component: str

    units_required: int

    urgency: str

    city: str

    latitude: float | None

    longitude: float | None

    request_status: str

    class Config:
        from_attributes = True