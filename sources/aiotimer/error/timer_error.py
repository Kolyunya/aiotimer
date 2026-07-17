class TimerError(Exception):
    """
    Base exception class for all other timer errors.
    """


class InvalidConfigurationError(TimerError):
    """
    Raised when a timer configuration is invalid.
    """
