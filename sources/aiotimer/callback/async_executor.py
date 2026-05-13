from asyncio import Lock, Task, create_task
from collections.abc import Awaitable, Callable

from typing_extensions import override

from ..event import ErrorEvent, EventType
from .callback import Callback
from .executor import Executor


class AsyncExecutor(Executor):

    @override
    def __init__(
        self,
        error_handler: Callback[ErrorEvent],
        error_factory: Callable[[Exception], Awaitable[ErrorEvent]],
    ) -> None:
        super().__init__(error_handler, error_factory)

        self.__lock = Lock()
        self.__tasks: list[Task[None]] = []

    async def __call__(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool = True,
    ) -> None:
        async with self.__lock:
            coroutine = self.__execute(
                callback,
                event,
                handle_errors=handle_errors,
            )

            task = create_task(coroutine)
            task.add_done_callback(self.__delete_task)
            self.__tasks.append(task)

    async def __execute(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool,
    ) -> None:
        try:
            await callback(event)
        except Exception as error:
            await self._handle_error(error, handle_errors=handle_errors)

    def __delete_task(self, task: Task[None]) -> None:
        self.__tasks.remove(task)
