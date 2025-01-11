from asynch import connect, connection
from asynch.cursors import DictCursor
from fastapi import FastAPI

from app.core.config import settings


async def init_clickhouse(state) -> None:  # pragma: no cover
    """
    Initialize clickhouse.

    :param app: current FastAPI application.
    """

    connection = await connect(dsn=str(settings.CLICKHOUSE_URL))

    state.clickhouse = connection


async def shutdown_clickhouse(state) -> None:  # pragma: no cover
    """
    Close all connection and pools.

    :param app: current application.
    """
    await state.clickhouse.close()
