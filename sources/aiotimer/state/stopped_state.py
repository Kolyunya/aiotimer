from typing_extensions import override

from .state import State


class StoppedState(State):

    @override
    def ensure_could_start(self) -> None:
        pass

    @override
    def ensure_could_reset(self) -> None:
        pass

    @override
    def ensure_could_adjust(self) -> None:
        pass
