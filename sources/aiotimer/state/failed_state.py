from typing_extensions import override

from .abstract_state import AbstractState


class FailedState(AbstractState):

    @override
    def ensure_could_reset(self) -> None:
        pass
