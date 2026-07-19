from abc import ABC
from asyncio import get_running_loop
from collections.abc import Awaitable, Callable

from typing_extensions import override

from ..event import ErrorEvent, EventType
from .callback import Callback
from .executor_interface import ExecutorInterface


class AbstractExecutor(ExecutorInterface, ABC):

    def __init__(
        self,
        error_handler: Callback[ErrorEvent],
        error_factory: Callable[[Exception], Awaitable[ErrorEvent]],
    ) -> None:
        self.__error_handler = error_handler
        self.__error_factory = error_factory

    @override
    async def handle_error(self, error: Exception, *, handle_errors: bool = True) -> None:
        if self.__error_handler.is_missing:
            self.__forward_error_to_event_loop(error, 'No error handler is provided')
            return

        if not handle_errors:
            self.__forward_error_to_event_loop(error, 'Error handler is disabled')
            return

        error_event = await self.__error_factory(error)

        await self.execute(
            self.__error_handler,
            error_event,

            # Disable error handling to prevent an infinite loop
            # in case an error occurs inside the error handler.
            handle_errors=False,
        )

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
            await self.handle_error(error, handle_errors=handle_errors)

    def __forward_error_to_event_loop(self, exception: Exception, message: str) -> None:
        loop = get_running_loop()
        loop.call_exception_handler({
            'exception': exception,
            'message': message,
        })
