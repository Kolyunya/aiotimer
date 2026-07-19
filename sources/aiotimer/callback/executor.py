from abc import ABC, abstractmethod
from asyncio import get_running_loop
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
    async def execute(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool = True,
    ) -> None:
        pass

    async def _execute(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool = True,
    ) -> None:
        try:
            await callback(event)
        except Exception as error:
            await self._handle_error(error, handle_errors=handle_errors)

    async def _handle_error(self, error: Exception, *, handle_errors: bool) -> None:
        if self.__error_handler.is_missing:
            self.__forward_error_to_loop(error, 'No error handler is provided')
            return

        if not handle_errors:
            self.__forward_error_to_loop(error, 'The error handler raised an exception')
            return

        error_event = await self.__error_factory(error)

        await self.execute(
            self.__error_handler,
            error_event,

            # Disable error handling to prevent an infinite loop
            # in case an error occurs inside the error handler.
            handle_errors=False,
        )

    def __forward_error_to_loop(self, exception: Exception, message: str) -> None:
        loop = get_running_loop()
        loop.call_exception_handler({
            'exception': exception,
            'message': message,
        })
