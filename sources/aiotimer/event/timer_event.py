from dataclasses import dataclass
from typing import TypeVar

from ..timer_interface import TimerInterface

EventType = TypeVar('EventType')


@dataclass(frozen=True)
class TimerEvent:
    """
    Base class for all timer-related events.

    This class provides the foundation for all timer events by including a reference
    to the timer that generated the event. All specific timer events inherit from
    this base class to provide consistent access to the timer instance.

    Attributes:
        timer: The timer instance that generated this event.
        elapsed: The elapsed time in seconds since the first interval started.
    """

    timer: TimerInterface
    elapsed: float
    remaining: float
