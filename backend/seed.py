"""
Seed script: populates sample data for the auto repair shop.
Run from the backend directory:  python seed.py
Safe to re-run: clears existing data first.
"""
from datetime import datetime, time, timedelta, date

from app.database import SessionLocal, engine, Base
from app import models

db = SessionLocal()


def clear_data():
    db.query(models.Appointment).delete()
    db.query(models.WorkingHours).delete()
    db.query(models.Service).delete()
    db.query(models.Mechanic).delete()
    db.commit()


def seed():
    clear_data()

    # --- Services (varying durations) ---
    oil_change = models.Service(name="Oil Change", duration_minutes=30, price=50)
    tire_rotation = models.Service(name="Tire Rotation", duration_minutes=30, price=100)
    brake_inspection = models.Service(name="Brake Inspection", duration_minutes=60, price=200)
    brake_replacement = models.Service(name="Brake Replacement", duration_minutes=120, price=350)
    db.add_all([oil_change, tire_rotation, brake_inspection, brake_replacement])
    db.commit()

    # --- Mechanics ---
    alex = models.Mechanic(name="Alex Carter")
    sam = models.Mechanic(name="Sam Rivera")
    db.add_all([alex, sam])
    db.commit()

    # --- Working hours: Mon–Fri 09:00–17:00 for both mechanics ---
    for mechanic in [alex, sam]:
        for weekday in range(0, 5):  # 0=Mon ... 4=Fri
            db.add(models.WorkingHours(
                mechanic_id=mechanic.id,
                day_of_week=weekday,
                start_time=time(9, 0),
                end_time=time(17, 0),
            ))
    db.commit()

    # --- Existing appointments (so availability has something to exclude) ---
    # Use the next Monday so the demo date is predictable.
    today = date.today()
    days_until_monday = (7 - today.weekday()) % 7 or 7
    next_monday = today + timedelta(days=days_until_monday)

    appts = [
        # Alex: oil change 09:00-09:30, brake inspection 10:00-11:00
        models.Appointment(
            service_id=oil_change.id, mechanic_id=alex.id,
            customer_name="Jordan Lee",
            start_time=datetime.combine(next_monday, time(9, 0)),
            end_time=datetime.combine(next_monday, time(9, 30)),
        ),
        models.Appointment(
            service_id=brake_inspection.id, mechanic_id=alex.id,
            customer_name="Priya Nair",
            start_time=datetime.combine(next_monday, time(10, 0)),
            end_time=datetime.combine(next_monday, time(11, 0)),
        ),
        # Sam: brake replacement 13:00-15:00
        models.Appointment(
            service_id=brake_replacement.id, mechanic_id=sam.id,
            customer_name="Chris Doyle",
            start_time=datetime.combine(next_monday, time(13, 0)),
            end_time=datetime.combine(next_monday, time(15, 0)),
        ),
    ]
    db.add_all(appts)
    db.commit()

    print(f"Seeded: 4 services, 2 mechanics, working hours Mon-Fri 9-5.")
    print(f"Sample appointments on {next_monday} (next Monday).")
    print(f"Try availability for mechanic {alex.id} / service {oil_change.id} / date {next_monday}")


if __name__ == "__main__":
    seed()
    db.close()