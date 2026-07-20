from asyncio import Task, create_task

from typing_extensions import override

from ...error.handler import ErrorHandlerInterface
from .abstract_executor import AbstractExecutor
from .executor_interface import Coroutine


class AsyncExecutor(AbstractExecutor):

    def __init__(self, error_handler: ErrorHandlerInterface) -> None:
        super().__init__(error_handler)

        self.__tasks: set[Task[None]] = set()

    @override
    async def _execute(self, coroutine: Coroutine) -> None:
        task = create_task(coroutine)
        task.add_done_callback(self.__delete_task)
        self.__tasks.add(task)

    def __delete_task(self, task: Task[None]) -> None:
        self.__tasks.remove(task)
