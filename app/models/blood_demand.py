from sqlalchemy import Column, Integer, Float, Date

from app.database.database import Base


class BloodDemandHistory(Base):

    __tablename__ = "blood_demand_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    date = Column(
        Date,
        nullable=False,
        unique=True,
        index=True
    )

    quantity_demanded = Column(
        Float,
        nullable=False
    )

    quantity_supplied = Column(
        Float,
        nullable=False
    )