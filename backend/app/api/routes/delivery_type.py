from fastapi import APIRouter

from app.api.deps import RedisDep, SessionDep
from app.dao import delivery_type_dao
from app.dto import DeliveryTypeDTO

router = APIRouter(tags=["delivery-type"], prefix="/delivery-type")


@router.get("", response_model=list[DeliveryTypeDTO])
async def get_list(
    db_session: SessionDep,
    redis: RedisDep,
) -> list[DeliveryTypeDTO]:
    items = await delivery_type_dao.get_all_cached(db_session, redis)
    return items
