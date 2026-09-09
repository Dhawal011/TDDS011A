from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.inventory import BloodInventory
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse
)


router = APIRouter(
    prefix="/inventory",
    tags=["Blood Inventory"]
)


@router.post(
    "/",
    response_model=InventoryResponse
)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    new_inventory = BloodInventory(
        blood_group=inventory.blood_group.value,
        blood_component=inventory.blood_component.value,
        units_available=inventory.units_available
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory


@router.get(
    "/",
    response_model=list[InventoryResponse]
)
def get_inventory(
    db: Session = Depends(get_db)
):

    return db.query(
        BloodInventory
    ).all()


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse
)
def get_inventory_item(
    inventory_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(
        BloodInventory
    ).filter(
        BloodInventory.id == inventory_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found"
        )

    return item