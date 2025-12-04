from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.image_tag import image_tag


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(10), unique=True, index=True, nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    folder = Column(String(255), nullable=True)
    url = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    size = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tags = relationship("Tag", secondary=image_tag, back_populates="images")

