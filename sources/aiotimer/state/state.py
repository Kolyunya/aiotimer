from ..error.state_error import InvalidStateError, InvalidStateNameError


class State:

    def __str__(self) -> str:
        class_name = self.__class__.__name__

        if not class_name.endswith('State'):
            raise InvalidStateNameError

        name = class_name.removesuffix('State')
        name = name.lower()

        return name

    def ensure_could_run(self) -> None:
        """Raise an exception if the timer could not been started."""
        self.__raise_error('run')

    def ensure_could_stop(self) -> None:
        """Raise an exception if the timer could not been stopped."""
        self.__raise_error('stopped')

    def ensure_could_reset(self) -> None:
        """Raise an exception if the timer could not be reset."""
        self.__raise_error('reset')

    def ensure_could_adjust(self) -> None:
        """Raise an exception if the timer could not be adjusted."""
        self.__raise_error('adjusted')

    def ensure_could_view(self) -> None:
        """
        Raise an exception if the remaining time could not be viewed.

        Note:
            No exception is raised in the current implementation.
            A user may view the remaining time at any state of the timer.
            The view_state() method always returns the current state type,
            while view() returns remaining time (0.0 if not running).
        """

    def __raise_error(self, operation: str) -> None:
        raise InvalidStateError(str(self), operation)
