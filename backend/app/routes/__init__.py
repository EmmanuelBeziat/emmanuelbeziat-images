from fastapi import APIRouter
from app.routes import images, tags, folders

api_router = APIRouter()

api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(folders.router, prefix="/folders", tags=["folders"])

