import pytest
from app.dao import user_dao
from app.dto import UserCreateDTO


from app.core.security import get_password_hash
from app.tests.utils.utils import random_email, random_lower_string
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.anyio


async def test_create_user(session: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateDTO(email=email, hashed_password=get_password_hash(password))
    user = await user_dao.create(session, user_in)

    assert user.email == email
    assert hasattr(user, "hashed_password")
