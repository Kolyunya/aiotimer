from dataclasses import dataclass

from ..timer_interface import TimerInterface


@dataclass(frozen=True)
class TimerEvent:
    """
    Base class for all timer-related events.

    This class provides the foundation for all timer events by including a reference
    to the timer that generated the event. All specific timer events inherit from
    this base class to provide consistent access to the timer instance.

    Attributes:
        timer: The timer instance that generated this event.
    """

    timer: TimerInterface
