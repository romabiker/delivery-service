from pydantic_core import from_json, to_json
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import DAOBase
from app.dto import DeliveryTypeCreateDTO, DeliveryTypeDTO, DeliveryTypeUpdateDTO
from app.models import DeliveryType


class DeliveryTypeDAO(
    DAOBase[DeliveryType, DeliveryTypeCreateDTO, DeliveryTypeUpdateDTO, DeliveryTypeDTO]
):
    async def get_all_cached(
        self,
        db: AsyncSession,
        redis: aioredis.Redis,
        expire: int = 3600,
        cache_key: str = "delivery_types:all",
    ) -> list[DeliveryTypeDTO]:
        """
        Provides DeliveryTypes from cache. If cache is expired then updates cache.
        """
        delivery_types_json = await redis.get(cache_key)
        if delivery_types_json is None:
            delivery_types = await self.get_all(db)
            await redis.set(
                cache_key,
                to_json(item.model_dump() for item in delivery_types),
                ex=expire,
            )
        else:
            delivery_types_dict_data = from_json(delivery_types_json)
            delivery_types = [
                self.item_dto_cls.model_construct(**item)
                for item in delivery_types_dict_data
            ]
        return delivery_types

    async def get_all_names(
        self,
        db: AsyncSession,
    ) -> list[str]:
        select_st = select(self.model.name)
        res = await db.execute(select_st)
        return list(res.scalars().all())

    async def get_all_ids(
        self,
        db: AsyncSession,
    ) -> list[int]:
        select_st = select(self.model.id)
        res = await db.execute(select_st)
        return list(res.scalars().all())

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[DeliveryTypeDTO]:
        select_st = select(self.model)
        res = await db.execute(select_st)
        return [self.item_dto_cls.model_validate(item) for item in res.scalars().all()]

    async def exists(self, db: AsyncSession, redis: aioredis.Redis, id_in: int) -> bool:
        delivery_types = await self.get_all_cached(db, redis)
        for delivery_type in delivery_types:
            if id_in == delivery_type.id:
                return True
        return False


delivery_type_dao = DeliveryTypeDAO(DeliveryType, DeliveryTypeDTO)
