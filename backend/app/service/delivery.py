import logging

from pydantic import ValidationError
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import delivery_dao, delivery_type_dao
from app.dto import DeliveryApiInDTO, DeliveryCreateDTO, DeliveryDTO, DeliveryTypeDTO
from app.service.base import ServiceBase

logger = logging.getLogger(__name__)


class CreateDeliveryService(ServiceBase):
    async def __call__(self, session: AsyncSession, redis: aioredis.Redis, delivery_in: DeliveryApiInDTO, user_id: int) -> DeliveryDTO:
        delivery_type_exists = await delivery_type_dao.exists(session, redis, delivery_in.type_id)
        if not delivery_type_exists:
            raise ValidationError(f'Delivery type does not exist: {delivery_in.type_id}')

        delivery_create_dto = DeliveryCreateDTO(**delivery_in.model_dump(), user_id=user_id)
        delivery_dto = await delivery_dao.create(session, delivery_create_dto)
        return delivery_dto



class DeliveryCalculateService(ServiceBase):
    async def __call__(self, redis: aioredis.Redis) -> list[DeliveryTypeDTO]: ...