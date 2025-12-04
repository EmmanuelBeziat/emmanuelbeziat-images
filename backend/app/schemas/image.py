from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ImageBase(BaseModel):
    folder: Optional[str] = None
    tags: Optional[List[int]] = []


class ImageCreate(ImageBase):
    pass


class ImageUpdate(BaseModel):
    filename: Optional[str] = None
    folder: Optional[str] = None
    tags: Optional[List[int]] = None


class TagResponse(BaseModel):
    id: int
    name: str
    slug: str
    color: Optional[str] = None

    class Config:
        from_attributes = True


class ImageResponse(BaseModel):
    id: int
    public_id: str
    filename: str
    original_filename: str
    folder: Optional[str] = None
    url: str
    mime_type: str
    size: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True

