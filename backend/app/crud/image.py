from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from app.models.image import Image
from app.models.tag import Tag
from app.schemas.image import ImageCreate, ImageUpdate
import random
import string


def generate_public_id(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_image(db: Session, public_id: str) -> Optional[Image]:
    return db.query(Image).filter(Image.public_id == public_id).first()


def get_images(
    db: Session,
    folder: Optional[str] = None,
    tags: Optional[List[int]] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Image]:
    query = db.query(Image)

    if folder:
        query = query.filter(Image.folder == folder)

    if tags:
        query = query.join(Image.tags).filter(Tag.id.in_(tags)).distinct()

    return query.offset(skip).limit(limit).all()


def create_image(db: Session, image_data: ImageCreate, filename: str, original_filename: str, url: str, mime_type: str, size: int) -> Image:
    public_id = generate_public_id()
    while db.query(Image).filter(Image.public_id == public_id).first():
        public_id = generate_public_id()

    db_image = Image(
        public_id=public_id,
        filename=filename,
        original_filename=original_filename,
        folder=image_data.folder,
        url=url,
        mime_type=mime_type,
        size=size
    )

    if image_data.tags:
        tags = db.query(Tag).filter(Tag.id.in_(image_data.tags)).all()
        db_image.tags = tags

    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_image(db: Session, public_id: str, image_update: ImageUpdate) -> Optional[Image]:
    db_image = get_image(db, public_id)
    if not db_image:
        return None

    if image_update.filename is not None:
        db_image.filename = image_update.filename

    if image_update.folder is not None:
        db_image.folder = image_update.folder

    if image_update.tags is not None:
        tags = db.query(Tag).filter(Tag.id.in_(image_update.tags)).all()
        db_image.tags = tags

    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, public_id: str) -> bool:
    db_image = get_image(db, public_id)
    if not db_image:
        return False

    db.delete(db_image)
    db.commit()
    return True


def get_folders(db: Session) -> List[str]:
    folders = db.query(Image.folder).filter(Image.folder.isnot(None)).distinct().all()
    return [folder[0] for folder in folders if folder[0]]

