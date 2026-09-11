from app.database.database import Base, engine, SessionLocal

from app.models.donor import Donor
from app.models.blood_request import BloodRequest
from app.models.inventory import BloodInventory


def seed_demo_data():

    # Make sure database tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        # ------------------------------------------------
        # Avoid duplicate demo data
        # ------------------------------------------------

        if db.query(Donor).count() > 0:

            print("Demo data already exists.")
            print("No new demo records were added.")
            return

        # ------------------------------------------------
        # DEMO DONORS
        # ------------------------------------------------

        donors = [

            Donor(
                name="Aarav Sharma",
                age=25,
                blood_group="O+",
                city="Mumbai",
                latitude=19.0760,
                longitude=72.8777,
                phone="9000000001",
                is_available=True
            ),

            Donor(
                name="Rohan Mehta",
                age=29,
                blood_group="O-",
                city="Mumbai",
                latitude=19.0330,
                longitude=73.0297,
                phone="9000000002",
                is_available=True
            ),

            Donor(
                name="Priya Shah",
                age=24,
                blood_group="A+",
                city="Mumbai",
                latitude=19.1136,
                longitude=72.8697,
                phone="9000000003",
                is_available=True
            ),

            Donor(
                name="Neha Patel",
                age=31,
                blood_group="B+",
                city="Mumbai",
                latitude=19.2183,
                longitude=72.9781,
                phone="9000000004",
                is_available=True
            ),

            Donor(
                name="Karan Joshi",
                age=27,
                blood_group="AB+",
                city="Mumbai",
                latitude=19.0178,
                longitude=73.0147,
                phone="9000000005",
                is_available=True
            ),

            Donor(
                name="Aditya Verma",
                age=35,
                blood_group="A-",
                city="Mumbai",
                latitude=19.0596,
                longitude=72.8295,
                phone="9000000006",
                is_available=False
            ),

            Donor(
                name="Sneha Kulkarni",
                age=26,
                blood_group="B-",
                city="Mumbai",
                latitude=19.0896,
                longitude=72.8656,
                phone="9000000007",
                is_available=True
            ),

            Donor(
                name="Vikram Rao",
                age=30,
                blood_group="AB-",
                city="Mumbai",
                latitude=19.0330,
                longitude=72.8570,
                phone="9000000008",
                is_available=True
            )
        ]

        db.add_all(donors)

        # ------------------------------------------------
        # DEMO BLOOD REQUESTS
        # ------------------------------------------------

        requests = [

            BloodRequest(
                hospital_name="City Care Hospital",
                blood_group="O+",
                blood_component="PACKED RBC",
                units_required=3,
                urgency="HIGH",
                city="Mumbai",
                latitude=19.0822,
                longitude=72.8811,
                request_status="PENDING"
            ),

            BloodRequest(
                hospital_name="Metro General Hospital",
                blood_group="A+",
                blood_component="PACKED RBC",
                units_required=2,
                urgency="CRITICAL",
                city="Mumbai",
                latitude=19.1197,
                longitude=72.9073,
                request_status="PENDING"
            ),

            BloodRequest(
                hospital_name="Sunrise Medical Center",
                blood_group="B+",
                blood_component="PLATELETS",
                units_required=4,
                urgency="NORMAL",
                city="Mumbai",
                latitude=19.0400,
                longitude=72.8500,
                request_status="PENDING"
            )
        ]

        db.add_all(requests)

        # ------------------------------------------------
        # DEMO INVENTORY
        # ------------------------------------------------

        inventory = [

            BloodInventory(
                blood_group="O+",
                blood_component="PACKED RBC",
                units_available=100
            ),

            BloodInventory(
                blood_group="O-",
                blood_component="PACKED RBC",
                units_available=35
            ),

            BloodInventory(
                blood_group="A+",
                blood_component="PACKED RBC",
                units_available=80
            ),

            BloodInventory(
                blood_group="A-",
                blood_component="PACKED RBC",
                units_available=20
            ),

            BloodInventory(
                blood_group="B+",
                blood_component="PACKED RBC",
                units_available=60
            ),

            BloodInventory(
                blood_group="B-",
                blood_component="PACKED RBC",
                units_available=15
            ),

            BloodInventory(
                blood_group="AB+",
                blood_component="PACKED RBC",
                units_available=25
            ),

            BloodInventory(
                blood_group="PLATELETS",
                blood_component="PLATELETS",
                units_available=40
            )
        ]

        db.add_all(inventory)

        db.commit()

        print()
        print("=" * 50)
        print("DEMO DATA CREATED SUCCESSFULLY")
        print("=" * 50)
        print()
        print("Donors added: 8")
        print("Blood requests added: 3")
        print("Inventory records added: 8")
        print()
        print("The application is ready for demonstration.")
        print()

    except Exception as e:

        db.rollback()

        print("Error while creating demo data:")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    seed_demo_data()