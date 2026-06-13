from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/", response_model=list[schemas.ServiceResponse])
def list_services(db: Session = Depends(get_db)):
    return crud.get_services(db)


@router.post("/", response_model=schemas.ServiceResponse)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, service)