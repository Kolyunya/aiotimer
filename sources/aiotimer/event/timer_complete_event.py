from dataclasses import dataclass

from .timer_event import TimerEvent


@dataclass(frozen=True)
class TimerCompleteEvent(TimerEvent):

    interval_count: int
