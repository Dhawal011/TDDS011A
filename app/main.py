from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.donor import Donor
from app.models.blood_request import BloodRequest

from app.api.donors import router as donor_router
from app.api.requests import router as request_router
from app.api.matching import router as matching_router
from app.api.prediction import router as prediction_router
from app.models.inventory import BloodInventory
from app.api.inventory import router as inventory_router
from app.models.blood_demand import BloodDemandHistory
from app.api.demand_history import router as demand_history_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blood Donor Matching API",
    description=(
        "An intelligent API for blood donor matching, "
        "blood inventory management and blood shortage prediction."
    ),
    version="1.0.0"
)


# Register routers
app.include_router(donor_router)
app.include_router(request_router)
app.include_router(matching_router)
app.include_router(prediction_router)
app.include_router(inventory_router)
app.include_router(demand_history_router)

@app.get("/")
def root():
    return {
        "message": "Blood Donor Matching API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Blood Donor Matching API",
        "version": "1.0.0"
    }