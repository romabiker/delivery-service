from fastapi import APIRouter

from app.api.routes import delivery, delivery_type, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(delivery.router)
api_router.include_router(delivery_type.router)
