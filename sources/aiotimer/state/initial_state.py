from typing_extensions import override

from .state import State


class InitialState(State):

    @override
    def ensure_could_run(self) -> None:
        pass

    @override
    def ensure_could_adjust(self) -> None:
        pass
