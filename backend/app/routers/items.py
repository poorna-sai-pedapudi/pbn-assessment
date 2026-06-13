from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.get("/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


@router.post("/", response_model=schemas.ItemResponse)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db)
):
    return crud.create_item(db, item)


@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    db: Session = Depends(get_db)
):
    updated_item = crud.update_item(
        db,
        item_id,
        item
    )

    if not updated_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return updated_item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    deleted_item = crud.delete_item(
        db,
        item_id
    )

    if not deleted_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {"message": "Item deleted successfully"}