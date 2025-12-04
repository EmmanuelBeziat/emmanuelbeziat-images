from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate
import re


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 100) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()


def get_tag_by_slug(db: Session, slug: str) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.slug == slug).first()


def create_tag(db: Session, tag_data: TagCreate) -> Tag:
    slug = slugify(tag_data.name)
    existing_tag = get_tag_by_slug(db, slug)
    if existing_tag:
        raise ValueError(f"Tag with name '{tag_data.name}' already exists")

    db_tag = Tag(
        name=tag_data.name,
        slug=slug,
        color=tag_data.color
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag_update: TagUpdate) -> Optional[Tag]:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None

    if tag_update.name is not None:
        slug = slugify(tag_update.name)
        existing_tag = get_tag_by_slug(db, slug)
        if existing_tag and existing_tag.id != tag_id:
            raise ValueError(f"Tag with name '{tag_update.name}' already exists")
        db_tag.name = tag_update.name
        db_tag.slug = slug

    if tag_update.color is not None:
        db_tag.color = tag_update.color

    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int) -> bool:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return False

    db.delete(db_tag)
    db.commit()
    return True

