from typing_extensions import override

from ..event import EventType
from .callback import Callback
from .executor import Executor


class SyncExecutor(Executor):

    @override
    async def execute(
        self,
        callback: Callback[EventType],
        event: EventType,
        *,
        handle_errors: bool = True,
    ) -> None:
        await self._execute(callback, event, handle_errors=handle_errors)
