from asyncio import get_running_loop
from collections.abc import Awaitable, Callable
from typing import Optional

from typing_extensions import override

from .error_handler_interface import ErrorHandlerInterface

Handler = Callable[[Exception], Awaitable[None]]


class ErrorHandler(ErrorHandlerInterface):

    def __init__(self, handler: Optional[Handler] = None) -> None:
        self.__handler = handler
        self.__loop = get_running_loop()

    @override
    async def handle(self, error: Exception) -> None:
        if self.__handler is None:
            await self.bubble(error)
            return

        try:
            await self.__handler(error)
        except Exception as handler_error:
            await self.bubble(error)
            await self.bubble(handler_error)

    @override
    async def bubble(self, error: Exception) -> None:
        context = {
            'exception': error,
            'message': str(error),
        }

        self.__loop.call_exception_handler(context)
