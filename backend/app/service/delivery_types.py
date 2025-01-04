import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import delivery_type_dao
from app.dto import DeliveryTypeCreateDTO
from app.service.base import ServiceBase

logger = logging.getLogger(__name__)


class CreateInitialDeliveryTypesService(ServiceBase):
    async def __call__(
        self, session: AsyncSession
    ):
        types_names = ['одежда', 'электроника', 'разное']
        names_exists = await delivery_type_dao.get_all_names(session)
        types_create = [DeliveryTypeCreateDTO(name=name) for name in types_names if name not in names_exists]
        if len(types_create):
            await delivery_type_dao.bulk_create(session, types_create)
