from __future__ import annotations

from abc import ABC, abstractmethod

from .state import StateInterface


class TimerInterface(ABC):

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
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
    def remaining(self) -> float:
        pass

    @property
    @abstractmethod
    def elapsed(self) -> float:
        pass

    @property
    @abstractmethod
    def state(self) -> type[StateInterface]:
        pass
