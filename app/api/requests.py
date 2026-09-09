from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.blood_request import BloodRequest
from app.schemas.blood_request import (
    BloodRequestCreate,
    BloodRequestResponse
)


router = APIRouter(
    prefix="/requests",
    tags=["Blood Requests"]
)


# --------------------------------------------------
# CREATE BLOOD REQUEST
# --------------------------------------------------

@router.post(
    "/",
    response_model=BloodRequestResponse
)
def create_blood_request(
    request: BloodRequestCreate,
    db: Session = Depends(get_db)
):

    new_request = BloodRequest(
        hospital_name=request.hospital_name,
        blood_group=request.blood_group.value,
        blood_component=request.blood_component.value,
        units_required=request.units_required,
        urgency=request.urgency.value,
        city=request.city,
        latitude=request.latitude,
        longitude=request.longitude,
        request_status="PENDING"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


# --------------------------------------------------
# GET ALL BLOOD REQUESTS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[BloodRequestResponse]
)
def get_all_requests(
    db: Session = Depends(get_db)
):

    requests = db.query(BloodRequest).all()

    return requests


# --------------------------------------------------
# GET REQUEST BY ID
# --------------------------------------------------

@router.get(
    "/{request_id}",
    response_model=BloodRequestResponse
)
def get_request(
    request_id: int,
    db: Session = Depends(get_db)
):

    blood_request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()

    if blood_request is None:
        raise HTTPException(
            status_code=404,
            detail="Blood request not found"
        )

    return blood_request


# --------------------------------------------------
# UPDATE REQUEST STATUS
# --------------------------------------------------

@router.patch(
    "/{request_id}/status",
    response_model=BloodRequestResponse
)
def update_request_status(
    request_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    blood_request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()

    if blood_request is None:
        raise HTTPException(
            status_code=404,
            detail="Blood request not found"
        )

    blood_request.request_status = status.upper()

    db.commit()
    db.refresh(blood_request)

    return blood_request