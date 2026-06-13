from datetime import datetime, timedelta, time as time_cls, date as date_cls
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func


# ---------- Service ----------
def get_services(db: Session):
    return db.query(models.Service).all()

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


# ---------- Mechanic ----------
def get_mechanics(db: Session):
    return db.query(models.Mechanic).all()

def get_mechanic(db: Session, mechanic_id: int):
    return db.query(models.Mechanic).filter(models.Mechanic.id == mechanic_id).first()

def create_mechanic(db: Session, mechanic: schemas.MechanicCreate):
    db_mechanic = models.Mechanic(**mechanic.model_dump())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic


# ---------- WorkingHours ----------
def get_working_hours_for_mechanic(db: Session, mechanic_id: int):
    return (
        db.query(models.WorkingHours)
        .filter(models.WorkingHours.mechanic_id == mechanic_id)
        .all()
    )

def create_working_hours(db: Session, wh: schemas.WorkingHoursCreate):
    db_wh = models.WorkingHours(**wh.model_dump())
    db.add(db_wh)
    db.commit()
    db.refresh(db_wh)
    return db_wh


# ---------- Appointment ----------
def get_appointments(db: Session):
    return db.query(models.Appointment).order_by(models.Appointment.start_time).all()

def get_available_slots(db: Session, mechanic_id: int, service_id: int, day):
    """
    Return bookable start times for a mechanic + service on a given date.
    A candidate slot is valid if it fits within the mechanic's working hours
    for that weekday and does not overlap any existing appointment.
    """
    service = get_service(db, service_id)
    if not service:
        return None  # router -> 404
    
     # Guard: no slots for past dates
    today = date_cls.today()
    if day < today:
        return []
    
    now = datetime.now()

    duration = timedelta(minutes=service.duration_minutes)
    step = timedelta(minutes=30)  # how often a slot can start

    # 1. Working hours for this weekday (0=Mon ... 6=Sun)
    weekday = day.weekday()
    hours = [
        wh for wh in get_working_hours_for_mechanic(db, mechanic_id)
        if wh.day_of_week == weekday
    ]
    if not hours:
        return []  # mechanic doesn't work this day

    # 2. Existing appointments that day (the ones we must avoid)
    existing = get_appointments_for_mechanic_on_date(db, mechanic_id, day)

    slots = []
    for wh in hours:
        window_start = datetime.combine(day, wh.start_time)
        window_end = datetime.combine(day, wh.end_time)

        candidate_start = window_start
        # 3. Walk the window in steps
        while candidate_start + duration <= window_end:
            candidate_end = candidate_start + duration

            # 4. Reject if it overlaps any existing appointment
            overlaps = any(
                candidate_start < appt.end_time and appt.start_time < candidate_end
                for appt in existing
            )

            # Skip slots in the past (for today's date)
            if day == today and candidate_start <= now:
                candidate_start += step
                continue

            if not overlaps:
                slots.append(
                    schemas.AvailableSlot(
                        start_time=candidate_start,
                        end_time=candidate_end,
                    )
                )

            candidate_start += step

    return slots

def get_appointments_for_mechanic_on_date(db: Session, mechanic_id: int, day):
    """All appointments for a mechanic that fall on a given date."""
    from datetime import datetime, time as time_cls
    day_start = datetime.combine(day, time_cls.min)   # 00:00
    day_end = datetime.combine(day, time_cls.max)     # 23:59:59
    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.mechanic_id == mechanic_id,
            models.Appointment.start_time >= day_start,
            models.Appointment.start_time <= day_end,
        )
        .all()
    )

def create_appointment(db: Session, appt: schemas.AppointmentCreate):
    service = get_service(db, appt.service_id)
    if not service:
        return {"error": "service_not_found"}

    start = appt.start_time
    end = start + timedelta(minutes=service.duration_minutes)

    # Conflict check: does this overlap an existing appointment for the same mechanic?
    existing = get_appointments_for_mechanic_on_date(db, appt.mechanic_id, start.date())
    conflict = any(
        start < a.end_time and a.start_time < end
        for a in existing
    )
    if conflict:
        return {"error": "slot_taken"}

    db_appt = models.Appointment(
        service_id=appt.service_id,
        mechanic_id=appt.mechanic_id,
        customer_name=appt.customer_name,
        start_time=start,
        end_time=end,
    )
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt

def delete_appointment(db: Session, appointment_id: int):
    db_appt = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not db_appt:
        return None  # router translates to 404

    db.delete(db_appt)
    db.commit()
    return db_appt

# ------------------------- DASHBOARD ---------------------------------------

def get_dashboard_stats(db: Session):
    """Aggregate booking insights for the provider dashboard."""

    # --- Most frequently booked services ---
    service_counts = (
        db.query(
            models.Service.name.label("name"),
            func.count(models.Appointment.id).label("count"),
        )
        .join(models.Appointment, models.Appointment.service_id == models.Service.id)
        .group_by(models.Service.name)
        .order_by(func.count(models.Appointment.id).desc())
        .all()
    )

    # --- Most common days of week ---
    # Postgres EXTRACT(DOW) returns 0=Sunday..6=Saturday
    day_counts_raw = (
        db.query(
            func.extract("dow", models.Appointment.start_time).label("dow"),
            func.count(models.Appointment.id).label("count"),
        )
        .group_by("dow")
        .all()
    )

    # Build a lookup from the raw counts: {dow_int: count}
    day_count_map = {int(r.dow): r.count for r in day_counts_raw}

    # Fixed display order: Mon–Fri first, then Sat, Sun
    # Postgres DOW: 0=Sun, 1=Mon, ... 6=Sat
    ordered_days = [
        (1, "Mon"), (2, "Tue"), (3, "Wed"), (4, "Thu"),
        (5, "Fri"), (6, "Sat"), (0, "Sun"),
    ]

    # --- Most common hours of day ---
    hour_counts_raw = (
        db.query(
            func.extract("hour", models.Appointment.start_time).label("hour"),
            func.count(models.Appointment.id).label("count"),
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    return {
        "services": [
            {"name": r.name, "count": r.count} for r in service_counts
        ],
        "days": [
            {"day": label, "count": day_count_map.get(dow, 0)}
            for dow, label in ordered_days
        ],
        "hours": [
            {"hour": f"{int(r.hour):02d}:00", "count": r.count}
            for r in hour_counts_raw
        ],
    }