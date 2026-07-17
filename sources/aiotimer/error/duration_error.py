from typing import Optional

from .timer_error import InvalidConfigurationError


class NegativeDurationError(InvalidConfigurationError):

    def __init__(self, message: Optional[str] = None) -> None:
        if not message:
            message = 'The duration must be a positive number or zero'
        super().__init__(message)


class InvalidDurationError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'Invalid duration provided'
        super().__init__(message)


class EmptyDurationIterableError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'Duration iterable must have at least one value'
        super().__init__(message)
