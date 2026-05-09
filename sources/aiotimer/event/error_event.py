from dataclasses import dataclass

from .timer_event import TimerEvent


@dataclass(frozen=True)
class ErrorEvent(TimerEvent):
    """
    Event that is fired when an error occurs during timer execution.

    This event is emitted when an exception occurs in timer operations,
    such as during callback execution or timer advancement. It provides
    access to the original exception for error handling and logging.

    Attributes:
        timer: The timer instance that generated this event.
        error: The exception that occurred during timer execution.

    Example:
        ```python
        def on_error(event: ErrorEvent):
            print(f"Timer error: {event.error}")
            # Log the error or take corrective action
        ```
    """

    error: Exception
