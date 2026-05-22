from time import monotonic
from typing import Optional

from ..error import (
    InvalidConfigurationError,
    InvalidDurationError,
    TimerError,
)


class Interval:

    def __init__(
        self,
        number: int,
        duration: float,
    ) -> None:
        self.__validate_number(number)
        self.__validate_duration(duration)

        self.__number: int = number
        self.__duration: float = duration

        self.__elapsed: float = 0.0
        self.__started_at: Optional[float] = None

    def start(self) -> None:
        if self.__started_at is not None:
            raise TimerError('The interval has already started')

        self.__started_at = monotonic()

    def stop(self) -> None:
        if self.__started_at is None:
            raise TimerError('The interval has not started yet')

        now = monotonic()
        elapsed = now - self.__started_at
        self.__elapsed += elapsed

        self.__started_at = None

    def prolong(self, delta: float) -> None:
        duration = self.__duration + delta
        self.duration = duration

    def shorten(self, delta: float) -> None:
        duration = self.__duration - delta
        self.duration = duration

    @property
    def number(self) -> int:
        return self.__number

    @property
    def duration(self) -> float:
        return self.__duration

    @duration.setter
    def duration(self, value: float) -> None:
        self.__validate_duration(value)
        self.__duration = value

    @property
    def remaining(self) -> float:
        remaining = self.__duration - self.elapsed

        return remaining

    @property
    def elapsed(self) -> float:
        elapsed = self.__elapsed

        if self.__started_at is not None:
            now = monotonic()
            elapsed += now - self.__started_at

        return elapsed

    @classmethod
    def __validate_number(cls, number: int) -> None:
        if number < 1:
            message = 'Interval numbers are one-based'
            raise InvalidConfigurationError(message)

    @classmethod
    def __validate_duration(cls, duration: float) -> None:
        if duration < 0:
            raise InvalidDurationError
