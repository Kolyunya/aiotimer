from collections.abc import Awaitable, Callable
from typing import Union

from ..event import IntervalCompleteEvent

OnIntervalComplete = Union[
    Callable[[], None],
    Callable[[], Awaitable[None]],
    Callable[[IntervalCompleteEvent], None],
    Callable[[IntervalCompleteEvent], Awaitable[None]],
]
