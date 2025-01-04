import logging

from redis import asyncio as aioredis
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def connect_redis():
    redis = aioredis.from_url(
        str(settings.REDIS_URL),
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        decode_responses=True,
        encoding="utf-8",
    )
    logger.info(f"Redis trying to connect: {settings.REDIS_URL}")
    try:
        await redis.ping()
        logger.info("Redis connected")
    except aioredis.RedisError as err:
        logger.error(str(err))
        raise err

    return redis
