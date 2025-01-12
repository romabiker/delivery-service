from typing import Annotated

from taskiq import Context, TaskiqDepends

from app.core.config import settings
from app.service import (
    DeliveryCalculateInBulkService,
    DeliveryCalculateService,
    DeliveryExportInClickhouseService,
)
from app.tkq import broker


@broker.task
async def delivery_calculate_task(
    delivery_id: int,
    context: Annotated[Context, TaskiqDepends()],
) -> bool:
    delivery_calculate = DeliveryCalculateService()
    is_ok = await delivery_calculate(delivery_id, context.state.redis)
    return is_ok


@broker.task(schedule=[{"cron": settings.DELIVERY_TASK_CALC_IN_BULK_CRON}])
async def delivery_calculate_in_bulk_task(
    context: Annotated[Context, TaskiqDepends()],
) -> None:
    delivery_calculate = DeliveryCalculateInBulkService(context.state.redis)
    await delivery_calculate()


@broker.task(schedule=[{"cron": settings.DELIVERY_TASK_EXPORT_IN_CLICKHOUSE_CRON}])
async def export_delivery_in_clickhouse(
    context: Annotated[Context, TaskiqDepends()],
) -> None:
    delivery_export = DeliveryExportInClickhouseService()
    await delivery_export(context.state.clickhouse)
