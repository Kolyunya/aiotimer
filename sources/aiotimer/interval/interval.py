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

        self.__elapsed: float = 0
        self.__advanced_at: Optional[float] = None

    def start(self) -> None:
        self.__advanced_at = monotonic()

    def stop(self) -> None:
        self.__advanced_at = None

    def advance(self) -> None:
        if self.__advanced_at is None:
            raise TimerError('Interval must be started before advancing')

        now = monotonic()

        elapsed = now - self.__advanced_at
        self.__elapsed += elapsed

        self.__advanced_at = now

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

        # The timer may (and will) overshoot
        # more or less depending on the precision value.
        # Return zero in case of an overshoot.
        remaining = max(remaining, 0)

        return remaining

    @property
    def elapsed(self) -> float:
        # The timer may (and will) overshoot
        # more or less depending on the precision value.
        # Return the duration value in case of an overshoot.
        elapsed = min(self.__elapsed, self.__duration)

        return elapsed

    @property
    def is_complete(self) -> bool:
        is_complete = self.__elapsed >= self.__duration

        return is_complete

    @classmethod
    def __validate_number(cls, number: int) -> None:
        if number < 1:
            message = 'Interval numbers are one-based'
            raise InvalidConfigurationError(message)

    @classmethod
    def __validate_duration(cls, duration: float) -> None:
        if duration < 0:
            raise InvalidDurationError
