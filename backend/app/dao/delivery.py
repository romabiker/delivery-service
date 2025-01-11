from collections.abc import Sequence
from typing import Any

from sqlalchemy import and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from app.dao.base import DAOBase
from app.dto import DeliveryCreateDTO, DeliveryDTO, DeliveryUpdateDTO
from app.dto.delivery import DeliveryTransportCompanyUpdateDTO
from app.models import Delivery


class DeliveryDAO(DAOBase[Delivery, DeliveryCreateDTO, DeliveryUpdateDTO, DeliveryDTO]):
    async def calculate_cost_of_delivery_rub(
        self,
        db: AsyncSession,
        usd_to_rub: float,
        delivery_id: int,
    ) -> bool:
        select_st = select(self.model).where(self.model.id == delivery_id)
        res = await db.execute(select_st)
        delivery = res.scalars().one_or_none()
        if delivery:
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
        select_st = (
            select(self.model)
            .where(and_(Delivery.cost_of_delivery_rub == 0))
            .order_by("id")
            .limit(batch_size)
        )
        res = await db.execute(select_st)
        deliveries = res.scalars().all()
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

    async def add_transport_company(
        self,
        db: AsyncSession,
        delivery_id: int,
        delivery_data: DeliveryTransportCompanyUpdateDTO,
    ) -> bool:
        """
        Добавляет транспортную компанию, если доставка не занята другой транспортной компанией
        """
        select_st = (
            select(self.model)
            .where(
                self.model.id == delivery_id, self.model.transport_company_id.is_(None)
            )
            .with_for_update(skip_locked=True)
        )
        res = await db.execute(select_st)
        delivery = res.scalars().one_or_none()
        if delivery:
            deliveries_update_data = [
                {
                    "id": delivery.id,
                    "transport_company_id": delivery_data.transport_company_id,
                }
            ]
            await db.execute(update(self.model), deliveries_update_data)
            await db.commit()
        return delivery is not None

    async def update_is_pushed_to_clickhouse(
        self,
        db: AsyncSession,
        deliveries_items: list[DeliveryDTO],
    ) -> None:
        deliveries_update_data = []
        for delivery in deliveries_items:
            deliveries_update_data.append(
                {
                    "id": delivery.id,
                    "is_pushed_to_clickhouse": True,
                }
            )
        if deliveries_update_data:
            await db.execute(update(Delivery), deliveries_update_data)
            await db.commit()


def calculate_cost_of_delivery(delivery: Delivery, usd_to_rub):
    return (delivery.weight_kg * 0.5 + delivery.cost_of_content_usd * 0.01) * usd_to_rub


delivery_dao = DeliveryDAO(Delivery, DeliveryDTO)
