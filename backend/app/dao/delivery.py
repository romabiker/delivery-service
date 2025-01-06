from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from app.dao.base import DAOBase
from app.dto import DeliveryCreateDTO, DeliveryDTO, DeliveryUpdateDTO
from app.models import Delivery


class DeliveryDAO(DAOBase[Delivery, DeliveryCreateDTO, DeliveryUpdateDTO, DeliveryDTO]):
    async def calculate_cost_of_delivery_rub(
        self,
        db: AsyncSession,
        usd_to_rub: float,
        delivery_id: int,
    ) -> bool:
        select_st = (
            select(self.model)
            .where(self.model.id == delivery_id)
            .with_for_update(skip_locked=True)
        )
        res = await db.execute(select_st)
        delivery = res.scalars().one_or_none()
        deliveries_update_data = [
            {
                "id": delivery.id,
                "cost_of_delivery_rub": calculate_cost_of_delivery(
                    delivery, usd_to_rub
                ),
            }
        ]

        await db.execute(update(self.model), deliveries_update_data)
        await db.commit()

        return delivery is not None

    async def calculate_cost_of_delivery_rub_in_bulk(
        self,
        db: AsyncSession,
        usd_to_rub: float,
        batch_size: int = 1000,
    ) -> int:
        deliveries = await self._select_for_update(
            db,
            filter_expr=and_(Delivery.cost_of_delivery_rub == 0),
            limit=batch_size,
            order="id",
        )
        deliveries_update_data = []
        for delivery in deliveries:
            deliveries_update_data.append(
                {
                    "id": delivery.id,
                    "cost_of_delivery_rub": calculate_cost_of_delivery(
                        delivery, usd_to_rub
                    ),
                }
            )
        if deliveries_update_data:
            await db.execute(update(self.model), deliveries_update_data)
            await db.commit()
        return len(deliveries_update_data)

    async def _select_for_update(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression[Any] | ColumnElement[Any] | None = None,
        skip: int = 0,
        limit: int = 100,
        order: str | None = None,
        skip_locked: bool = True,
    ) -> Sequence[Delivery]:
        select_st = select(self.model).with_for_update(skip_locked=skip_locked)

        if filter_expr is not None:
            select_st = select_st.where(filter_expr)

        if order is not None:
            select_st = select_st.order_by(order)

        if skip is not None:
            select_st = select_st.offset(skip)

        if limit is not None:
            select_st = select_st.limit(limit)

        res = await db.execute(select_st)
        return res.scalars().all()


def calculate_cost_of_delivery(delivery: Delivery, usd_to_rub):
    return (delivery.weight_kg * 0.5 + delivery.cost_of_content_usd * 0.01) * usd_to_rub


delivery_dao = DeliveryDAO(Delivery, DeliveryDTO)
