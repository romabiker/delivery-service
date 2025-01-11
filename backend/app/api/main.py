from fastapi import APIRouter

from app.api.routes import delivery, delivery_type, transport_company, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(delivery.router)
api_router.include_router(delivery_type.router)
api_router.include_router(transport_company.router)
