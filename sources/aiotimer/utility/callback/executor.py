from asyncio import Lock, Task, create_task
from collections.abc import Callable
from typing import TypeVar

from ...event import ErrorEvent
from .callback import Callback

EventType = TypeVar('EventType')


class Executor:

    def __init__(
        self,
        error_handler: Callback[ErrorEvent],
        error_factory: Callable[[Exception], ErrorEvent],
    ) -> None:
        self.__error_handler = error_handler
        self.__error_factory = error_factory

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
            if not handle_errors or not self.__error_handler.is_set:
                raise

            error_event = self.__error_factory(error)

            await self(
                self.__error_handler,
                error_event,

                # Disable error handling to prevent an infinite loop
                # in case an error occurs inside the error handler.
                handle_errors=False,
            )

    def __delete_task(self, task: Task[None]) -> None:
        self.__tasks.remove(task)
