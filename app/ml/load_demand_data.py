import pandas as pd

from app.database.database import (
    Base,
    engine,
    SessionLocal
)

from app.models.blood_demand import BloodDemandHistory

DATA_PATH = "data/processed/blood_demand_clean.csv"


def load_demand_data():

    df = pd.read_csv(DATA_PATH)

    df["DATE"] = pd.to_datetime(df["DATE"])
    
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            existing = db.query(
                BloodDemandHistory
            ).filter(
                BloodDemandHistory.date == row["DATE"].date()
            ).first()

            if existing:
                skipped += 1
                continue

            record = BloodDemandHistory(
                date=row["DATE"].date(),
                quantity_demanded=float(
                    row["QTY_DEMANDED"]
                ),
                quantity_supplied=float(
                    row["QTY_SUPPLIED"]
                )
            )

            db.add(record)
            inserted += 1

        db.commit()

        print("Demand data loaded successfully.")
        print(f"Records inserted: {inserted}")
        print(f"Records skipped: {skipped}")

    finally:

        db.close()


if __name__ == "__main__":
    load_demand_data()