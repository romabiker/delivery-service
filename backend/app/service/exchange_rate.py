import logging
from json import JSONDecodeError
from typing import Final

import httpx
from multidict import CIMultiDict
from redis import asyncio as aioredis
from redis.asyncio.lock import Lock
from redis.exceptions import LockError

from ..utils.common import float_or_none
from .base import ServiceBase

logger = logging.getLogger(__name__)


class GetUsdExсhangeRateService(ServiceBase):
    """
    Предоставляет актуальный курс доллара к рублю. Данные берутся из открытых источников в интернете.
    Используется кеширование для хранения и блокировка на внешний http запрос и обновлении данных в кеше.
    """
    base_headers: dict = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU;q=0.8,ru;q=0.7",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    }
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    lock_name: Final[str] = "usd_to_rub:update:lock"
    # макс срок жизни блокировки
    timeout_sec = 20
    # макс количество времени, потраченное на попытку получить блокировку
    blocking_timeout_sec = 0

    usd_to_rub_redis_key: Final[str] = "usd_to_rub:value"
    usd_to_rub_redis_key_expire_sec = 60 * 60  # 1 h
    usd_to_rub_redis_reserve_key: Final[str] = "usd_to_rub:reserve:value"

    def __init__(
        self,
        redis: aioredis.Redis,
        headers: dict | None = None,
        connect_timeout: float = 5.0,
        retries=2,
    ):
        self.timeout = httpx.Timeout(10.0, connect=connect_timeout)
        self.transport = httpx.AsyncHTTPTransport(retries=retries, verify=False)

        self.headers = CIMultiDict(
            self.base_headers
        )  # case insensitive multidict instance
        if headers:
            self.headers.update(headers)
        self.client_kwargs = {
            "headers": dict(self.headers),
            "transport": self.transport,
            "timeout": self.timeout,
            "follow_redirects": True,
        }

        self.redis: aioredis.Redis = redis
        self.lock: Lock | None = None

    async def __call__(self) -> float | None:
        usd_to_rub_str = await self.redis.get(self.usd_to_rub_redis_key)
        usd_to_rub = float_or_none(usd_to_rub_str)
        if usd_to_rub:
            return usd_to_rub

        if not await self.acquire_lock():
            usd_to_rub_str = await self.redis.get(self.usd_to_rub_redis_reserve_key)
            return float_or_none(usd_to_rub_str)

        exchange_data = await self.get_exchange_data()
        usd_to_rub = exchange_data.get("Valute", {}).get("USD", {}).get("Value")
        if usd_to_rub:
            await self.redis.set(
                self.usd_to_rub_redis_key,
                usd_to_rub,
                ex=self.usd_to_rub_redis_key_expire_sec,
            )
            await self.redis.set(self.usd_to_rub_redis_reserve_key, usd_to_rub)
            logger.info('Updated usd_to_rub cache')
        else:
            logger.error('usd_to_rub is not found in exchange_data: %s', exchange_data)
        await self.release_lock()
        
        return usd_to_rub

    async def get_exchange_data(self) -> dict:
        async with httpx.AsyncClient(**self.client_kwargs) as client:  # type: ignore[arg-type]
            try:
                resp = await client.get(self.url)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as error:
                logger.error("Http Error updating usd exchange rate: %s", str(error))
            except JSONDecodeError as error:
                logger.error(
                    "Json Decode Error parsing usd exchange rate response: `%s` - %s", resp.text, str(error)
                )

    async def acquire_lock(self) -> bool:
        """Получить блокировку операции"""

        self.lock = self.redis.lock(
            self.lock_name,
            timeout=self.timeout_sec,
            blocking_timeout=self.blocking_timeout_sec,
        )
        return await self.lock.acquire()

    async def release_lock(self) -> None:
        """Освободить блокировку операции"""
        if self.lock is not None:
            try:
                await self.lock.release()
            except LockError:
                pass
