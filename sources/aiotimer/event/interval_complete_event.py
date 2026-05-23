from dataclasses import dataclass

from .timer_event import TimerEvent


@dataclass(frozen=True)
class IntervalCompleteEvent(TimerEvent):

    interval_number: int

    interval_duration: float
