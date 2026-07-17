from dataclasses import dataclass

from .timer_event import TimerEvent


@dataclass(frozen=True)
class ErrorEvent(TimerEvent):

    error: Exception
