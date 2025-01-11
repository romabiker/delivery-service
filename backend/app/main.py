from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.core.clickhouse.lifespan import init_clickhouse, shutdown_clickhouse
from app.core.config import settings
from app.core.db import async_engine
from app.core.rabbit.lifespan import init_rabbit, shutdown_rabbit
from app.core.redis import connect_redis


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.tkq import broker

    await init_clickhouse(app.state)
    app.state.redis = await connect_redis()
    init_rabbit(app)
    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()

    await shutdown_clickhouse(app.state)
    await shutdown_rabbit(app)
    await async_engine.dispose()
    await app.state.redis.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)


app.include_router(api_router, prefix=settings.API_V1_STR)
