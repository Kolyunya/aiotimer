from .timer_error import InvalidConfigurationError


class EmptyGeneratorError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'The interval generator must yield at least one value'
        super().__init__(message)
