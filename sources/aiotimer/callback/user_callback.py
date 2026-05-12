from collections.abc import Awaitable, Callable
from typing import Optional, TypeVar, Union

from ..event import ErrorEvent, IntervalCompleteEvent, TimerCompleteEvent

EventType = TypeVar('EventType')

ParameterizedUserCallback = Union[
    Callable[[EventType], None],
    Callable[[EventType], Awaitable[None]],
]

ParameterlessUserCallback = Union[
    Callable[[], None],
    Callable[[], Awaitable[None]],
]

UserCallback = Optional[
    Union[
        ParameterizedUserCallback[EventType],
        ParameterlessUserCallback,
    ]
]

OnIntervalComplete = UserCallback[IntervalCompleteEvent]
OnTimerComplete = UserCallback[TimerCompleteEvent]
OnError = UserCallback[ErrorEvent]

UserCallbackResult = Optional[Awaitable[None]]
