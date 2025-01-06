import logging

from pydantic import ValidationError
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_maker
from app.dao import delivery_dao, delivery_type_dao
from app.dto import DeliveryApiInDTO, DeliveryCreateDTO, DeliveryDTO
from app.service.base import ServiceBase
from app.service.exchange_rate import GetUsdExсhangeRateService

logger = logging.getLogger(__name__)


class CreateDeliveryService(ServiceBase):
    async def __call__(
        self,
        session: AsyncSession,
        redis: aioredis.Redis,
        delivery_in: DeliveryApiInDTO,
        user_id: int,
    ) -> DeliveryDTO:
        delivery_type_exists = await delivery_type_dao.exists(
            session, redis, delivery_in.type_id
        )
        if not delivery_type_exists:
            raise ValidationError(
                f"Delivery type does not exist: {delivery_in.type_id}"
            )

        delivery_create_dto = DeliveryCreateDTO(
            **delivery_in.model_dump(), user_id=user_id
        )
        delivery_dto = await delivery_dao.create(session, delivery_create_dto)
        return delivery_dto


class DeliveryCalculateService(ServiceBase):
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def __call__(self) -> None:
        logger.info("Starting calculate deliveries")
        get_usd_exchange_rate = GetUsdExсhangeRateService(self.redis)
        usd_to_rub = await get_usd_exchange_rate()
        if usd_to_rub is None:
            logger.error(
                "Stopped cost of deliveries calculation because usd_to_rub rate was not obtained"
            )
            return

        batch_size = 1000

        async with async_session_maker() as session:
            while True:
                calculated_items = (
                    await delivery_dao.calculate_cost_of_delivery_rub_in_bulk(
                        session, usd_to_rub, batch_size
                    )
                )
                logger.info("Calculated {} deliveries")
                if calculated_items == 0:
                    break

        logger.info("Finished calculating deliveries")
