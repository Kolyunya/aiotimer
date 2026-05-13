from dataclasses import dataclass

from .timer_event import TimerEvent


@dataclass(frozen=True)
class IntervalCompleteEvent(TimerEvent):
    """
    Event that is fired when an individual timer interval completes.

    This event is emitted each time a single interval in the timer's interval sequence
    completes. It provides information about the specific interval that just completed,
    including its number in the sequence and its actual duration.

    Attributes:
        timer: The timer instance that generated this event.
        elapsed: The elapsed time in seconds since the first interval started.
        interval_number: The 1-based index of the completed interval in the sequence.
        interval_duration: The actual duration of the completed interval in seconds.

    Example:
        ```python
        def on_interval_complete(event: IntervalCompleteEvent):
            print(f"Interval {event.interval_number} completed after {event.interval_duration}s")
        ```
    """

    interval_number: int
    interval_duration: float
