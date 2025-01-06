from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_maker


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_async_redis(rq: Request) -> aioredis.Redis:
    return rq.app.state.redis


RedisDep = Annotated[aioredis.Redis, Depends(get_async_redis)]
