from abc import ABC, abstractmethod
from typing import Any


class ServiceBase(ABC):
    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Any: ...  # type:ignore[no-untyped-def]
