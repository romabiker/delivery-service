from app.dto import UserDTO
from app.service.base import ServiceBase
import logging

logger = logging.getLogger(__name__)


class RegisterOrLoginUserService(ServiceBase):
    
    
    async def __call__(self, uuid: str | None) -> tuple[bool, UserDTO] | tuple[bool, str]:
        
        if uuid is None:
            ...
        else:
            
            ...
        return