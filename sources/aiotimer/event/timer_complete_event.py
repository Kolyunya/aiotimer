from dataclasses import dataclass

from .timer_event import TimerEvent


@dataclass(frozen=True)
class TimerCompleteEvent(TimerEvent):
    """
    Event that is fired when the last of timer's intervals completes.

    This event is generated once when the timer's entire sequence of intervals
    completes. It provides summary information about the total number of
    intervals that were executed during the timer's lifecycle.

    Attributes:
        timer: The timer instance that generated this event.
        elapsed: The elapsed time in seconds since the first interval started.
        interval_count: The total number of intervals that were executed.

    Example:
        ```python
        def on_timer_complete(event: TimerCompleteEvent):
            print(f"Timer completed after {event.interval_count} intervals")
        ```
    """

    interval_count: int
