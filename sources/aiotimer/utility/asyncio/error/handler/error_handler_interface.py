from abc import ABC, abstractmethod


class ErrorHandlerInterface(ABC):

    @abstractmethod
    async def handle(self, error: Exception) -> None:
        pass

    @abstractmethod
    async def bubble(self, error: Exception) -> None:
        pass
