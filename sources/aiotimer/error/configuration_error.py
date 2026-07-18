from .timer_error import TimerError


class InvalidConfigurationError(TimerError):
    """
    Raised when a timer configuration is invalid.
    """
