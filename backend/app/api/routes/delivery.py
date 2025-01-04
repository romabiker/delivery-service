from typing import Annotated

from fastapi import APIRouter, Cookie, HTTPException, Query, Request, Response
from sqlalchemy import and_

from app.api.deps import RedisDep, SessionDep
from app.api.pagination import paginate_by_page_number
from app.dao import delivery_dao
from app.dto import DeliveryApiInDTO, DeliveryDTO, DeliveryPageNumberPagination
from app.models import Delivery
from app.service import CreateDeliveryService, RegisterOrLoginUserService

router = APIRouter(tags=["delivery"], prefix="/delivery")


@router.post("", status_code=201, response_model=DeliveryDTO)
async def update_or_create(
    delivery_in: DeliveryApiInDTO,
    response: Response,
    db_session: SessionDep,
    redis: RedisDep,
    session_id: Annotated[str | None, Cookie()] = None,
) -> DeliveryDTO:
    """
    Register or login user from session_id request cookies. Create delivery.
    Return delivery_dto.id
    """

    register_or_login_user = RegisterOrLoginUserService()
    user_dto = await register_or_login_user(db_session, session_id)
    response.set_cookie(key="session_id", value=user_dto.session)
    create_delivery = CreateDeliveryService()
    delivery_dto = await create_delivery(db_session, redis, delivery_in, user_dto.id)
    return delivery_dto


@router.get("", response_model=DeliveryPageNumberPagination)
async def get_list(
    response: Response,
    db_session: SessionDep,
    request: Request,
    session_id: Annotated[str | None, Cookie()] = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=100, ge=1, le=1000),
    order: str = Query(default="id"),
    delivery_type_id: int | None = Query(default=None),
    is_calculated: bool | None = Query(default=None)
) -> DeliveryPageNumberPagination:
    register_or_login_user = RegisterOrLoginUserService()
    user_dto = await register_or_login_user(db_session, session_id)
    response.set_cookie(key="session_id", value=user_dto.session)

    filters = (Delivery.user_id == user_dto.id)
    if delivery_type_id:
        filters &= (Delivery.type_id == delivery_type_id)
    if is_calculated is True:
        filters &= (Delivery.cost_of_delivery_rub > 0)
    if is_calculated is False:
        filters &= (Delivery.cost_of_delivery_rub == 0)

    total = await delivery_dao.count(db_session, filter_expr=filters)
    items = []
    if total:
        items = await delivery_dao.get_list(
            db_session,
            filter_expr=filters,
            skip=(page - 1) * per_page, limit=per_page, order=order
        )
    return paginate_by_page_number(request, items, total, page, per_page)


@router.get("/{delivery_id}", response_model=DeliveryDTO)
async def get(
    delivery_id: int,
    response: Response,
    db_session: SessionDep,
    session_id: Annotated[str | None, Cookie()] = None,
) -> DeliveryDTO:
    register_or_login_user = RegisterOrLoginUserService()
    user_dto = await register_or_login_user(db_session, session_id)
    response.set_cookie(key="session_id", value=user_dto.session)

    filters = and_(Delivery.user_id == user_dto.id, Delivery.id == delivery_id)
    delivery_dto = await delivery_dao.get(db_session, filter_expr=filters)
    if not delivery_dto:
        raise HTTPException(status_code=404, detail="Not found")
    return delivery_dto

