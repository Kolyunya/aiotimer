from typing_extensions import override

from .abstract_executor import AbstractExecutor
from .executor_interface import Coroutine


class SyncExecutor(AbstractExecutor):

    @override
    async def _execute(self, coroutine: Coroutine) -> None:
        await coroutine
