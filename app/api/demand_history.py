from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.blood_demand import BloodDemandHistory


router = APIRouter(
    prefix="/demand-history",
    tags=["Demand History"]
)


@router.get("/")
def get_demand_history(
    db: Session = Depends(get_db)
):

    records = db.query(
        BloodDemandHistory
    ).order_by(
        BloodDemandHistory.date
    ).all()

    return [
        {
            "date": record.date,
            "quantity_demanded": record.quantity_demanded,
            "quantity_supplied": record.quantity_supplied
        }
        for record in records
    ]