from abc import ABC

from typing_extensions import override

from ..error.state_error import InvalidStateError, InvalidStateNameError
from .state_interface import StateInterface


class AbstractState(StateInterface, ABC):

    @override
    def __str__(self) -> str:
        class_name = self.__class__.__name__

        if not class_name.endswith('State'):
            raise InvalidStateNameError

        name = class_name.removesuffix('State')
        name = name.lower()

        return name

    @override
    def ensure_could_start(self) -> None:
        self.__raise_error('started')

    @override
    def ensure_could_stop(self) -> None:
        self.__raise_error('stopped')

    @override
    def ensure_could_reset(self) -> None:
        self.__raise_error('reset')

    @override
    def ensure_could_adjust(self) -> None:
        self.__raise_error('adjusted')

    def __raise_error(self, operation: str) -> None:
        raise InvalidStateError(str(self), operation)
