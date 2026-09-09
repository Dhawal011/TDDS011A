from sqlalchemy import Column, Integer, String, Boolean, Float

from app.database.database import Base


class Donor(Base):

    __tablename__ = "donors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    blood_group = Column(
        String,
        nullable=False,
        index=True
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

    phone = Column(
        String,
        nullable=False
    )

    is_available = Column(
        Boolean,
        default=True
    )