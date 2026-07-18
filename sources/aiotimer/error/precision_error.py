from .configuration_error import InvalidConfigurationError


class InvalidPrecisionError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'The precision must be a positive number'
        super().__init__(message)
