from typing import Any

import taskiq_fastapi
from taskiq import (
    AsyncBroker,
    AsyncResultBackend,
    TaskiqEvents,
    TaskiqScheduler,
    TaskiqState,
)
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from app.core.clickhouse.lifespan import init_clickhouse, shutdown_clickhouse
from app.core.config import settings
from app.core.db import async_engine
from app.core.redis import connect_redis

result_backend: AsyncResultBackend[Any] = RedisAsyncResultBackend(
    redis_url=str(settings.REDIS_URL.with_path("/1")),
)


broker: AsyncBroker = AioPikaBroker(str(settings.RABBIT_URL)).with_result_backend(
    result_backend
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    # Here we store connection pool on startup for later use.
    state.redis = await connect_redis()
    await init_clickhouse(state)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    # Here we close our pool on shutdown event.
    await state.redis.disconnect()
    await async_engine.dispose()
    await state.redis.close()
    await shutdown_clickhouse(state)


scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


taskiq_fastapi.init(
    broker,
    "app.main:app",
)
