from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from ..event import ErrorEvent, EventType
from .callback import Callback


class Executor(ABC):

    def __init__(
        self,
        error_handler: Callback[ErrorEvent],
        error_factory: Callable[[Exception], Awaitable[ErrorEvent]],
    ) -> None:
        self.__error_handler = error_handler
        self.__error_factory = error_factory

    @abstractmethod
    async def __call__(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool = True,
    ) -> None:
        pass

    async def _handle_error(self, error: Exception, *, handle_errors: bool) -> None:
        if not handle_errors or self.__error_handler.is_missing:
            raise error

        error_event = await self.__error_factory(error)

        await self(
            self.__error_handler,
            error_event,

            # Disable error handling to prevent an infinite loop
            # in case an error occurs inside the error handler.
            handle_errors=False,
        )
