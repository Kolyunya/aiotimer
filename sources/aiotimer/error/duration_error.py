from typing import Optional

from .timer_error import InvalidConfigurationError


class InvalidDurationError(InvalidConfigurationError):

    def __init__(self, message: Optional[str] = None) -> None:
        if not message:
            message = 'The duration must be a positive number or zero'
        super().__init__(message)
