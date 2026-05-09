from .timer_error import TimerError


class InvalidStateError(TimerError):

    def __init__(self, state: str, operation: str) -> None:
        message = f'The timer could not be {operation} while in the {state} state'
        super().__init__(message)


class InvalidStateNameError(TimerError):

    def __init__(self) -> None:
        message = 'The state class name must end with `State`'
        super().__init__(message)
