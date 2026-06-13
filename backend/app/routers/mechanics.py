from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/mechanics", tags=["Mechanics"])


@router.get("/", response_model=list[schemas.MechanicResponse])
def list_mechanics(db: Session = Depends(get_db)):
    return crud.get_mechanics(db)


@router.post("/", response_model=schemas.MechanicResponse)
def create_mechanic(mechanic: schemas.MechanicCreate, db: Session = Depends(get_db)):
    return crud.create_mechanic(db, mechanic)