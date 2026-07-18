from .configuration_error import InvalidConfigurationError


class MissingCallbackError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'At least one of the `on_interval_complete` and `on_timer_complete` callbacks must be specified'
        super().__init__(message)
