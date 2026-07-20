from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Any


class JobQueueInterface(ABC):

    @abstractmethod
    async def push(self, job: Awaitable[Any]) -> None:
        pass

    @abstractmethod
    async def process(self) -> None:
        pass
