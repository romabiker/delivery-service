import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import user_dao
from app.dto import UserCreateDTO

pytestmark = pytest.mark.anyio


async def test_create_user(db_session: AsyncSession) -> None:
    user_session_uuid = str(uuid.uuid4())
    user_dto = await user_dao.create(
        db_session,
        UserCreateDTO.model_construct(session=user_session_uuid),
    )

    assert hasattr(user_dto, "session")
    assert user_dto.user_session_uuid == user_session_uuid
    assert user_dto.id is not None
