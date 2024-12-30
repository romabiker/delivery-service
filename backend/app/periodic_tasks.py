import logging
from asyncio import run

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    from app.service import InitDbService

    init_db = InitDbService()
    await init_db()


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    run(main())
