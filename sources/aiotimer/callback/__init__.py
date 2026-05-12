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

from .callback import Callback
from .executor import Executor
from .user_callback import OnError, OnIntervalComplete, OnTimerComplete

__all__ = [
    'Callback',
    'Executor',
    'OnError',
    'OnIntervalComplete',
    'OnTimerComplete',
]
