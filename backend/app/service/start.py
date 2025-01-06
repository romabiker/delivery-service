import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.service.base import ServiceBase

from .delivery_types import CreateInitialDeliveryTypesService

logger = logging.getLogger(__name__)


class InitDbService(ServiceBase):
    async def __call__(self, session: AsyncSession) -> None:
        create_initial_delivery_types = CreateInitialDeliveryTypesService()
        await create_initial_delivery_types(session)
        return
