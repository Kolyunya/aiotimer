from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import State


class TimerInterface(ABC):

    @abstractmethod
    async def run(self) -> None:
        pass

    @abstractmethod
    async def pause(self) -> None:
        pass

    @abstractmethod
    async def reset(self) -> None:
        pass

    @abstractmethod
    async def set(self, duration: float) -> None:
        pass

    @abstractmethod
    async def prolong(self, delta: float) -> None:
        pass

    @abstractmethod
    async def shorten(self, delta: float) -> None:
        pass

    @property
    @abstractmethod
    async def remaining_time(self) -> float:
        pass

    @property
    @abstractmethod
    async def elapsed_time(self) -> float:
        pass

    @property
    @abstractmethod
    async def state(self) -> type[State]:
        pass
