from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/working-hours", tags=["Working Hours"])


@router.get("/{mechanic_id}", response_model=list[schemas.WorkingHoursResponse])
def list_working_hours(mechanic_id: int, db: Session = Depends(get_db)):
    return crud.get_working_hours_for_mechanic(db, mechanic_id)


@router.post("/", response_model=schemas.WorkingHoursResponse)
def create_working_hours(wh: schemas.WorkingHoursCreate, db: Session = Depends(get_db)):
    return crud.create_working_hours(db, wh)