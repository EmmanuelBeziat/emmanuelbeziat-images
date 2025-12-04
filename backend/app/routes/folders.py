from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud

router = APIRouter()


@router.get("", response_model=List[str])
def get_folders(db: Session = Depends(get_db)):
    folders = crud.image.get_folders(db=db)
    return folders

