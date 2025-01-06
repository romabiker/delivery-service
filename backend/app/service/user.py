import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import user_dao
from app.dto import UserCreateDTO, UserDTO
from app.service.base import ServiceBase

logger = logging.getLogger(__name__)


class RegisterOrLoginUserService(ServiceBase):
    async def __call__(
        self,
        db_session: AsyncSession,
        session_uuid: str | None,
        full_name: str | None = None,
    ) -> UserDTO:
        user_dto = None
        if session_uuid is not None:
            user_dto = await user_dao.get_by_uuid(db_session, session_uuid)

        if user_dto is None:
            user_dto = await user_dao.create(
                db_session,
                UserCreateDTO.model_construct(
                    session=str(uuid.uuid4()), full_name=full_name
                ),
            )
        return user_dto
