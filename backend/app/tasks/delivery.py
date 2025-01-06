from typing import Annotated

from taskiq import Context, TaskiqDepends

from app.service.delivery import (
    DeliveryCalculateInBulkService,
    DeliveryCalculateService,
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


@broker.task(schedule=[{"cron": "*/5 * * * *"}])
async def delivery_calculate_in_bulk_task(
    context: Annotated[Context, TaskiqDepends()],
) -> None:
    delivery_calculate = DeliveryCalculateInBulkService(context.state.redis)
    await delivery_calculate()
