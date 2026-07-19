from abc import ABC, abstractmethod


class StateInterface(ABC):

    @abstractmethod
    def ensure_could_start(self) -> None:
        """
        Raise an exception if the timer could not been started.
        """

    @abstractmethod
    def ensure_could_stop(self) -> None:
        """
        Raise an exception if the timer could not been stopped.
        """

    @abstractmethod
    def ensure_could_reset(self) -> None:
        """
        Raise an exception if the timer could not be reset.
        """

    @abstractmethod
    def ensure_could_adjust(self) -> None:
        """
        Raise an exception if the timer could not be adjusted.
        """
