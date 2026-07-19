from typing_extensions import override

from .abstract_state import AbstractState


class InitialState(AbstractState):

    @override
    def ensure_could_start(self) -> None:
        pass

    @override
    def ensure_could_adjust(self) -> None:
        pass
