from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .interval import once
from .multi_timer import MultiTimer

if TYPE_CHECKING:
    from .callback import (
        OnError,
        OnTimerComplete,
    )


class Timer(MultiTimer):

    def __init__(
        self,
        duration: float,
        on_timer_complete: Optional[OnTimerComplete] = None,
        on_error: Optional[OnError] = None,
    ) -> None:
        super().__init__(
            once(duration),
            on_timer_complete=on_timer_complete,
            on_interval_complete=None,
            on_error=on_error,
        )
