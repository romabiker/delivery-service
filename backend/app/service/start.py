from app.dto import UserDTO
from app.service.base import ServiceBase
import logging

logger = logging.getLogger(__name__)


class InitDbService(ServiceBase):
    async def __call__(
        self
    ) -> tuple[bool, UserDTO] | tuple[bool, str]:
        return
