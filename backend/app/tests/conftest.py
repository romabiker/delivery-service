# ruff: noqa: ARG001
# mypy: disable-error-code="no-untyped-def,type-arg"
import asyncio

import pytest
from app.api.deps import get_async_session
from app.models import User, TronWallet
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete


from app.core.config import settings
from app.main import app
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.db import create_engine_kwargs
from starlette.requests import Request


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop(request: Request):
    # https://github.com/pytest-dev/pytest-asyncio/issues/68
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def session_maker(anyio_backend):
    engine_kwargs = create_engine_kwargs()
    engine_kwargs['echo'] = False
    async_engine = create_async_engine(**create_engine_kwargs())
    async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    await clear_db(async_session_maker)

    yield async_session_maker
    
    await clear_db(async_session_maker)

    await async_engine.dispose()


@pytest.fixture(scope="session")
async def client(session_maker: async_sessionmaker):
    async def override_get_async_session():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url=f'http://0.0.0.0:8000{settings.API_V1_STR}') as async_client:
        yield async_client


@pytest.fixture(scope="session")
async def session(session_maker: async_sessionmaker):
    async with session_maker() as session:
        yield session


async def clear_db(session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        await session.execute(delete(User))
        await session.execute(delete(TronWallet))
        await session.commit()
