from .timer_error import InvalidConfigurationError


class EmptyGeneratorError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'The interval generator yielded no values'
        super().__init__(message)
