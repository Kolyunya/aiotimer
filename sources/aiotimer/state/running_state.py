from typing_extensions import override

from .abstract_state import AbstractState


class RunningState(AbstractState):

    @override
    def ensure_could_stop(self) -> None:
        pass

    @override
    def ensure_could_reset(self) -> None:
        pass

    @override
    def ensure_could_adjust(self) -> None:
        pass
