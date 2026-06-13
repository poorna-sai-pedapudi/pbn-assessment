from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/dashboard")
def dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)