from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date as date_type
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=list[schemas.AppointmentResponse])
def list_appointments(db: Session = Depends(get_db)):
    return crud.get_appointments(db)

@router.get("/availability/", response_model=list[schemas.AvailableSlot])
def get_availability(
    mechanic_id: int,
    service_id: int,
    date: date_type,
    db: Session = Depends(get_db),
):
    slots = crud.get_available_slots(db, mechanic_id, service_id, date)
    if slots is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return slots


@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    result = crud.create_appointment(db, appt)

    if isinstance(result, dict):
        if result.get("error") == "service_not_found":
            raise HTTPException(status_code=404, detail="Service not found")
        if result.get("error") == "slot_taken":
            raise HTTPException(
                status_code=409,
                detail="That time slot is no longer available.",
            )

    return result


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_appointment(db, appointment_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment cancelled successfully"}