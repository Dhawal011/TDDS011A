from enum import Enum

from pydantic import BaseModel, Field, field_validator


class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class DonorCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ...,
        ge=18,
        le=65
    )

    blood_group: BloodGroup

    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    latitude: float | None = None

    longitude: float | None = None

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15
    )

    @field_validator("blood_group", mode="before")
    @classmethod
    def normalize_blood_group(cls, value):
        return value.upper()


class DonorResponse(BaseModel):

    id: int

    name: str

    age: int

    blood_group: str

    city: str

    latitude: float | None

    longitude: float | None

    phone: str

    is_available: bool

    class Config:
        from_attributes = True