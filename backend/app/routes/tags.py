from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud
from app.schemas.tag import TagResponse, TagCreate, TagUpdate

router = APIRouter()


@router.get("", response_model=List[TagResponse])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.tag.get_tags(db=db, skip=skip, limit=limit)
    return tags


@router.post("", response_model=TagResponse, status_code=201)
def create_tag(tag_data: TagCreate, db: Session = Depends(get_db)):
    try:
        db_tag = crud.tag.create_tag(db=db, tag_data=tag_data)
        return db_tag
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag_update: TagUpdate, db: Session = Depends(get_db)):
    try:
        db_tag = crud.tag.update_tag(db=db, tag_id=tag_id, tag_update=tag_update)
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return db_tag
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    success = crud.tag.delete_tag(db=db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None

