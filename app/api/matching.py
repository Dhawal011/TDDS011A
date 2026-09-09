from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.donor import Donor
from app.models.blood_request import BloodRequest

from app.services.matching_service import (
    get_compatible_donor_groups,
    calculate_distance_km,
    calculate_match_score
)


router = APIRouter(
    prefix="/matching",
    tags=["Donor Matching"]
)


@router.get("/find/{request_id}")
def find_matching_donors(
    request_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # 1. FIND BLOOD REQUEST
    # --------------------------------------------------

    blood_request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()

    if blood_request is None:

        raise HTTPException(
            status_code=404,
            detail="Blood request not found"
        )


    # --------------------------------------------------
    # 2. GET COMPATIBLE BLOOD GROUPS
    # --------------------------------------------------

    compatible_groups = get_compatible_donor_groups(
        blood_request.blood_group
    )

    if not compatible_groups:

        return {
            "request_id": request_id,
            "matches": [],
            "message": "No compatible blood groups found."
        }


    # --------------------------------------------------
    # 3. FIND AVAILABLE DONORS
    # --------------------------------------------------

    donors = db.query(Donor).filter(
        Donor.is_available == True,
        Donor.blood_group.in_(compatible_groups)
    ).all()


    matches = []


    # --------------------------------------------------
    # 4. CALCULATE DISTANCE + SCORE
    # --------------------------------------------------

    for donor in donors:

        distance = calculate_distance_km(
            blood_request.latitude,
            blood_request.longitude,
            donor.latitude,
            donor.longitude
        )

        score = calculate_match_score(
            distance,
            blood_request.urgency
        )

        matches.append({

            "donor_id": donor.id,

            "donor_name": donor.name,

            "blood_group": donor.blood_group,

            "city": donor.city,

            "distance_km": (
                round(distance, 2)
                if distance is not None
                else None
            ),

            "is_available": donor.is_available,

            "match_score": score
        })


    # --------------------------------------------------
    # 5. SORT BY SCORE
    # --------------------------------------------------

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )


    # --------------------------------------------------
    # 6. RETURN RESULT
    # --------------------------------------------------

    return {

        "request_id": request_id,

        "requested_blood_group":
            blood_request.blood_group,

        "urgency":
            blood_request.urgency,

        "compatible_donor_groups":
            compatible_groups,

        "total_matches":
            len(matches),

        "matches":
            matches
    }