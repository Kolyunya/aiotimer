from collections.abc import Awaitable, Callable
from typing import Union

from ..event import TimerCompleteEvent

OnTimerComplete = Union[
    Callable[[], None],
    Callable[[], Awaitable[None]],
    Callable[[TimerCompleteEvent], None],
    Callable[[TimerCompleteEvent], Awaitable[None]],
]
