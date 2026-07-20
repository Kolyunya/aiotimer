from abc import ABC, abstractmethod
from collections.abc import Coroutine as AsyncioCoroutine
from typing import Any

Coroutine = AsyncioCoroutine[Any, Any, None]


class ExecutorInterface(ABC):

    @abstractmethod
    async def execute(
        self,
        coroutine: Coroutine,
        *,
        bubble_errors: bool = False,
    ) -> None:
        pass
