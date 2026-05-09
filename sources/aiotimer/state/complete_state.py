from typing_extensions import override

from .state import State


class CompleteState(State):

    @override
    def ensure_could_reset(self) -> None:
        pass
