from typing_extensions import override

from ..event import EventType
from .callback import Callback
from .executor import Executor


class SyncExecutor(Executor):

    @override
    async def __call__(
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
