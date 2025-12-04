from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app import crud
from app.schemas.image import ImageResponse, ImageUpdate
from app.config import settings
import os
import shutil
import uuid
from pathlib import Path

router = APIRouter()


@router.post("/upload", response_model=ImageResponse, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    folder: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    if file.content_type not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    file_content = await file.read()
    file_size = len(file_content)

    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    upload_dir = Path(settings.UPLOAD_DIR)
    if folder:
        upload_dir = upload_dir / folder

    upload_dir.mkdir(parents=True, exist_ok=True)

    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    relative_url = str(file_path.relative_to(Path(settings.UPLOAD_DIR)))
    if os.sep != "/":
        relative_url = relative_url.replace(os.sep, "/")

    tag_ids = []
    if tags:
        tag_ids = [int(t.strip()) for t in tags.split(",") if t.strip()]

    from app.schemas.image import ImageCreate
    image_data = ImageCreate(folder=folder, tags=tag_ids)

    db_image = crud.image.create_image(
        db=db,
        image_data=image_data,
        filename=unique_filename,
        original_filename=file.filename,
        url=relative_url,
        mime_type=file.content_type,
        size=file_size
    )

    return db_image


@router.get("", response_model=List[ImageResponse])
def get_images(
    folder: Optional[str] = None,
    tags: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tag_ids = None
    if tags:
        tag_ids = [int(t) for t in tags.split(",")]

    images = crud.image.get_images(db=db, folder=folder, tags=tag_ids, skip=skip, limit=limit)
    return images


@router.get("/{public_id}", response_model=ImageResponse)
def get_image(public_id: str, db: Session = Depends(get_db)):
    db_image = crud.image.get_image(db, public_id=public_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.put("/{public_id}", response_model=ImageResponse)
def update_image(
    public_id: str,
    image_update: ImageUpdate,
    db: Session = Depends(get_db)
):
    db_image = crud.image.update_image(db=db, public_id=public_id, image_update=image_update)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.delete("/{public_id}", status_code=204)
def delete_image(public_id: str, db: Session = Depends(get_db)):
    success = crud.image.delete_image(db=db, public_id=public_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return None

