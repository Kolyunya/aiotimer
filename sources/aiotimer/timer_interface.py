from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from typing_extensions import Self

if TYPE_CHECKING:
    from .state import State


class TimerInterface(ABC):

    @abstractmethod
    async def run(self) -> Self:
        pass

    @abstractmethod
    async def pause(self) -> Self:
        pass

    @abstractmethod
    async def reset(self) -> Self:
        pass

    @abstractmethod
    async def set(self, duration: float) -> Self:
        pass

    @abstractmethod
    async def prolong(self, duration_delta: float) -> Self:
        pass

    @abstractmethod
    async def shorten(self, duration_delta: float) -> Self:
        pass

    @abstractmethod
    async def view(self) -> float:
        pass

    @abstractmethod
    async def view_state(self) -> type[State]:
        pass
