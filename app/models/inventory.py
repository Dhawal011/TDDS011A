from sqlalchemy import Column, Integer, String

from app.database.database import Base


class BloodInventory(Base):

    __tablename__ = "blood_inventory"

    id = Column(
        Integer,
        primary_key=True,
        index=True
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

    units_available = Column(
        Integer,
        nullable=False,
        default=0
    )