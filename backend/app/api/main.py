from fastapi import APIRouter

from app.api.routes import delivery, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(delivery.router)
