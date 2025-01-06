import logging
from asyncio import run

from app.core.db import async_session_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    from app.service import InitDbService

    init_db = InitDbService()
    async with async_session_maker() as session:
        try:
            await init_db(session)
        except Exception as err:
            logger.error("Initial data was not created created due: %s", str(err))
            raise err
        finally:
            await session.close()


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    run(main())
