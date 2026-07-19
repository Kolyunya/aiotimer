from abc import ABC, abstractmethod

from ..event import EventType
from .callback import Callback


class ExecutorInterface(ABC):

    @abstractmethod
    async def execute(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool = True,
    ) -> None:
        pass
