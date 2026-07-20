from abc import ABC, abstractmethod

from typing_extensions import override

from ...error.handler import ErrorHandlerInterface
from .executor_interface import Coroutine, ExecutorInterface


class AbstractExecutor(ExecutorInterface, ABC):

    def __init__(self, error_handler: ErrorHandlerInterface) -> None:
        self.__error_handler = error_handler

    @override
    async def execute(
        self,
        coroutine: Coroutine,
        *,
        bubble_errors: bool = False,
    ) -> None:
        coroutine = self.__handle_errors(coroutine, bubble_errors=bubble_errors)
        await self._execute(coroutine)

    @abstractmethod
    async def _execute(self, coroutine: Coroutine) -> None:
        pass

    async def __handle_errors(self, coroutine: Coroutine, *, bubble_errors: bool) -> None:
        try:
            await coroutine

        except Exception as error:
            if bubble_errors:
                handle_error_coroutine = self.__error_handler.bubble(error)
            else:
                handle_error_coroutine = self.__error_handler.handle(error)

            # Enable error-bubbling to the event loop.
            # Failing to do so results in an infinite loop inside a failing error handler.
            await self.execute(handle_error_coroutine, bubble_errors=True)
