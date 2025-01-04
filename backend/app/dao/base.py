from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, func, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from app.models.base import AsyncBase


class DAOBase[
    ModelType: AsyncBase,
    CreateDTO: BaseModel,
    UpdateDTO: BaseModel,
    ItemDTO: BaseModel,
]:
    def __init__(self, model: type[ModelType], item_dto_cls: type[ItemDTO]):
        """
        DAO generic base class with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `model`: A Pydantic BaseModel model class
        """
        self.model = model
        self.item_dto_cls = item_dto_cls

    async def get(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression[Any] | ColumnElement[Any],
    ) -> ItemDTO | None:
        res = await db.execute(select(self.model).where(filter_expr))
        orm_obj = res.scalars().one_or_none()
        if orm_obj:
            return self.item_dto_cls.model_validate(orm_obj)

    async def get_list(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression[Any] | ColumnElement[Any] | None = None,
        skip: int = 0,
        limit: int = 100,
        order: str | None = None,
    ) -> list[ItemDTO]:
        select_st = select(self.model)
        if filter_expr is not None:
            select_st = select_st.where(filter_expr)

        if order is not None:
            select_st = select_st.order_by(order)

        if skip is not None:
            select_st = select_st.offset(skip)

        if limit is not None:
            select_st = select_st.limit(limit)

        res = await db.execute(select_st)
        return [
            self.item_dto_cls.model_validate(orm_obj) for orm_obj in res.scalars().all()
        ]

    async def create(self, db: AsyncSession, obj_in: CreateDTO) -> ItemDTO:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return self.item_dto_cls.model_validate(db_obj)

    async def update(
        self,
        db: AsyncSession,
        filter_expr: BinaryExpression[Any] | ColumnElement[Any],
        obj_in: UpdateDTO,
    ) -> ItemDTO | None:
        update_st = update(self.model).where(filter_expr).values(**obj_in.model_dump())
        await db.execute(update_st)
        await db.commit()
        return await self.get(db, filter_expr)

    async def remove(
        self, db: AsyncSession, filter_expr: BinaryExpression[Any] | ColumnElement[Any]
    ) -> None:
        await db.execute(delete(self.model).where(filter_expr))
        await db.commit()
        return

    async def bulk_remove(
        self, db: AsyncSession, filter_expr: BinaryExpression[Any] | ColumnElement[Any]
    ) -> None:
        await db.execute(delete(self.model).where(filter_expr))
        await db.commit()
        return

    async def count(
        self, db: AsyncSession, filter_expr: BinaryExpression[Any] | ColumnElement[Any] | None = None
    ) -> int:
        select_st = select(func.count(self.model.id))

        if filter_expr is not None:
            select_st = select_st.where(filter_expr)

        res = await db.execute(select_st)
        return res.scalar_one()

    async def bulk_create(self, db: AsyncSession, objects_in: list[CreateDTO]) -> None:
        await db.execute(insert(self.model), [obj.model_dump() for obj in objects_in])
        await db.commit()
        return
