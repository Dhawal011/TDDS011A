from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class BloodRequest(Base):

    __tablename__ = "blood_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hospital_name = Column(
        String,
        nullable=False
    )

    blood_group = Column(
        String,
        nullable=False,
        index=True
    )

    blood_component = Column(
        String,
        nullable=False
    )

    units_required = Column(
        Integer,
        nullable=False
    )

    urgency = Column(
        String,
        nullable=False
    )

    city = Column(
        String,
        nullable=False
    )

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )

    request_status = Column(
        String,
        nullable=False,
        default="PENDING"
    )