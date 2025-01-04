import asyncio
import logging
from asyncio import run

from app.core.redis import connect_redis
from app.service.delivery import DeliveryCalculateService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    redis = await connect_redis()
    delivery_calculate = DeliveryCalculateService(redis)
    while True:
        await delivery_calculate()
        await asyncio.sleep(5000)


if __name__ == "__main__":
    run(main())
