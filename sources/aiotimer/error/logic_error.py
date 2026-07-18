from .timer_error import TimerError


class LogicError(TimerError):
    """
    Raised from code paths that are expected to be unreachable.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
