import logging

from asynch.cursors import DictCursor
from pydantic import ValidationError
from redis import asyncio as aioredis
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_maker
from app.dao import delivery_dao, delivery_type_dao
from app.dto import (
    DeliveryApiInDTO,
    DeliveryClickHouseStats,
    DeliveryCreateDTO,
    DeliveryDTO,
    DeliveryExportInClickhouseDTO,
)
from app.models import Delivery
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


class DeliveryCalculateInBulkService(ServiceBase):
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def __call__(self) -> int | None:
        logger.info("Starting calculate deliveries")
        get_usd_exchange_rate = GetUsdExсhangeRateService(self.redis)
        usd_to_rub = await get_usd_exchange_rate()
        if usd_to_rub is None:
            logger.error(
                "Stopped cost of deliveries calculation because usd_to_rub rate was not obtained"
            )
            return None

        batch_size = 1000
        calculated_cnt = 0

        async with async_session_maker() as session:
            while True:
                calculated = await delivery_dao.calculate_cost_of_delivery_rub_in_bulk(
                    session, usd_to_rub, batch_size
                )
                calculated_cnt += calculated
                logger.info(f"Calculated deliveries: {calculated}")
                if calculated == 0:
                    break

        logger.info(f"All calculated deliveries: {calculated_cnt}")
        logger.info("Finished calculating deliveries")
        return calculated_cnt


class DeliveryCalculateService(ServiceBase):
    async def __call__(self, delivery_id: int, redis: aioredis.Redis) -> bool:
        get_usd_exchange_rate = GetUsdExсhangeRateService(redis)
        usd_to_rub = await get_usd_exchange_rate()
        if usd_to_rub is None:
            logger.error(
                "Stopped cost of deliveries calculation for delivery#:%s because usd_to_rub rate was not obtained",
                delivery_id,
            )
            return False

        async with async_session_maker() as session:
            is_calculated = await delivery_dao.calculate_cost_of_delivery_rub(
                session, usd_to_rub, delivery_id
            )
        return is_calculated


class DeliveryExportInClickhouseService(ServiceBase):
    delivery_columns = "type_id,transport_company_id,weight_kg,cost_of_content_usd,cost_of_delivery_rub,created_at"
    insert_sql = f"INSERT INTO deliveries ({delivery_columns}) VALUES"

    async def __call__(self, clickhouse, batch_size: int = 1000) -> None:
        logger.info("Start export in Clickhouse")
        while True:
            async with async_session_maker() as session:
                deliveries_items = await delivery_dao.get_list(
                    session,
                    and_(
                        Delivery.is_pushed_to_clickhouse == False,
                        Delivery.cost_of_delivery_rub >= 0,
                        Delivery.transport_company_id.is_not(None),
                    ),
                    order="id",
                    limit=batch_size,
                )
                if not deliveries_items:
                    break

                deliveries_out = [
                    DeliveryExportInClickhouseDTO.model_validate(item).model_dump()
                    for item in deliveries_items
                ]
                async with clickhouse.cursor(cursor=DictCursor) as cursor:
                    await cursor.execute(
                        self.insert_sql,
                        deliveries_out,
                    )
                await delivery_dao.update_is_pushed_to_clickhouse(
                    session, deliveries_items
                )
                logger.info(f"Exported {len(deliveries_items)} items")

        logger.info("Finished export in Clickhouse")


class DeliveryStatsService(ServiceBase):
    async def __call__(self, clickhouse) -> list[DeliveryClickHouseStats]:
        async with clickhouse.cursor(cursor=DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT
                    date_trunc('day', created_at) as created,
                    type_id,
                    SUM(cost_of_delivery_rub) AS total_cost
                FROM
                    deliveries
                GROUP BY
                    created, type_id
                ORDER BY created ASC;
                """
            )
        return await cursor.fetchall()
