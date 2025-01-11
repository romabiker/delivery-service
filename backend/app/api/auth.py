from typing import Annotated

from fastapi import Cookie, Depends, Response

from app.api.deps import SessionDep
from app.core.config import settings
from app.dto import UserDTO
from app.service import RegisterOrLoginUserService


async def login_or_register_by_cookie(
    response: Response,
    db_session: SessionDep,
    session_id: Annotated[str | None, Cookie()] = None,
) -> UserDTO:
    register_or_login_user = RegisterOrLoginUserService()
    user_dto = await register_or_login_user(db_session, session_id)
    response.set_cookie(
        key="session_id", value=user_dto.session, expires=settings.AUTH_COOKIE_EXPIRE
    )
    return user_dto


UserByCookieDep = Annotated[UserDTO, Depends(login_or_register_by_cookie)]
