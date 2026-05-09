"""
Callback Function Types.

Types:
    OnIntervalComplete: Callback function that is called
        each time any timer interval completes.

    OnTimerComplete: Callback function that is called
        each time the last timer interval completes.

    OnError: Callback function that is called
        each time when timer encounters an error.
"""

from .on_error import OnError
from .on_interval_complete import OnIntervalComplete
from .on_timer_complete import OnTimerComplete

__all__ = [
    'OnError',
    'OnIntervalComplete',
    'OnTimerComplete',
]
