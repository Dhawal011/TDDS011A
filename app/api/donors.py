from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.donor import Donor
from app.schemas.donor import DonorCreate, DonorResponse


router = APIRouter(
    prefix="/donors",
    tags=["Donors"]
)


# --------------------------------------------------
# CREATE DONOR
# --------------------------------------------------

@router.post(
    "/",
    response_model=DonorResponse
)
def create_donor(
    donor: DonorCreate,
    db: Session = Depends(get_db)
):

    new_donor = Donor(
        name=donor.name,
        age=donor.age,
        blood_group=donor.blood_group.upper(),
        city=donor.city,
        latitude=donor.latitude,
        longitude=donor.longitude,
        phone=donor.phone
    )

    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)

    return new_donor


# --------------------------------------------------
# GET ALL DONORS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[DonorResponse]
)
def get_all_donors(
    db: Session = Depends(get_db)
):

    donors = db.query(Donor).all()

    return donors


# --------------------------------------------------
# GET DONOR BY ID
# --------------------------------------------------

@router.get(
    "/{donor_id}",
    response_model=DonorResponse
)
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db)
):

    donor = db.query(Donor).filter(
        Donor.id == donor_id
    ).first()

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    return donor


# --------------------------------------------------
# UPDATE DONOR AVAILABILITY
# --------------------------------------------------

@router.patch(
    "/{donor_id}/availability",
    response_model=DonorResponse
)
def update_availability(
    donor_id: int,
    is_available: bool,
    db: Session = Depends(get_db)
):

    donor = db.query(Donor).filter(
        Donor.id == donor_id
    ).first()

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    donor.is_available = is_available

    db.commit()
    db.refresh(donor)

    return donor


# --------------------------------------------------
# DELETE DONOR
# --------------------------------------------------

@router.delete(
    "/{donor_id}"
)
def delete_donor(
    donor_id: int,
    db: Session = Depends(get_db)
):

    donor = db.query(Donor).filter(
        Donor.id == donor_id
    ).first()

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    db.delete(donor)
    db.commit()

    return {
        "message": "Donor deleted successfully",
        "donor_id": donor_id
    }