from ..error.state_error import InvalidStateError, InvalidStateNameError


class State:

    def __str__(self) -> str:
        class_name = self.__class__.__name__

        if not class_name.endswith('State'):
            raise InvalidStateNameError

        name = class_name.removesuffix('State')
        name = name.lower()

        return name

    def ensure_could_start(self) -> None:
        """Raise an exception if the timer could not been started."""
        self.__raise_error('started')

    def ensure_could_stop(self) -> None:
        """Raise an exception if the timer could not been stopped."""
        self.__raise_error('stopped')

    def ensure_could_reset(self) -> None:
        """Raise an exception if the timer could not be reset."""
        self.__raise_error('reset')

    def ensure_could_adjust(self) -> None:
        """Raise an exception if the timer could not be adjusted."""
        self.__raise_error('adjusted')

    def __raise_error(self, operation: str) -> None:
        raise InvalidStateError(str(self), operation)
