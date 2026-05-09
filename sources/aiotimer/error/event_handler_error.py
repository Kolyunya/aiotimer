from .timer_error import InvalidConfigurationError


class MissingEventHandlerError(InvalidConfigurationError):

    def __init__(self) -> None:
        message = 'At least one of the `on_interval_complete` and `on_timer_complete` event handlers must be specified'
        super().__init__(message)
