from collections.abc import Awaitable, Callable
from typing import Union

from ..event import ErrorEvent

OnError = Union[
    Callable[[], None],
    Callable[[], Awaitable[None]],
    Callable[[ErrorEvent], None],
    Callable[[ErrorEvent], Awaitable[None]],
]
