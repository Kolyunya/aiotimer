from time import monotonic_ns
from typing import Optional

from ..error import (
    InvalidConfigurationError,
    NegativeDurationError,
    TimerError,
)
from ..utility.time import ns2s, s2ns


class Interval:

    def __init__(
        self,
        number: int,
        duration: float,
    ) -> None:
        self.__validate_number(number)
        self.__validate_duration(duration)

        self.__number: int = number
        self.__duration: int = s2ns(duration)

        self.__elapsed: int = 0
        self.__advanced_at: Optional[int] = None

    def start(self) -> None:
        self.__advanced_at = monotonic_ns()

    def stop(self) -> None:
        self.__advanced_at = None

    def advance(self) -> None:
        if self.__advanced_at is None:
            raise TimerError('Interval must be started before advancing')

        now = monotonic_ns()

        elapsed = now - self.__advanced_at
        self.__elapsed += elapsed

        self.__advanced_at = now

    def prolong(self, delta: float) -> None:
        self.__adjust(delta)

    def shorten(self, delta: float) -> None:
        self.__adjust(-1 * delta)

    @property
    def number(self) -> int:
        return self.__number

    @property
    def duration(self) -> float:
        return ns2s(self.__duration)

    @duration.setter
    def duration(self, value: float) -> None:
        self.__validate_duration(value)
        self.__duration = s2ns(value)

    @property
    def remaining(self) -> float:
        remaining_ns = self.__duration - self.__elapsed

        # The timer may (and will) overshoot
        # more or less depending on the precision value.
        # Return zero in case of an overshoot.
        remaining_ns = max(remaining_ns, 0)

        remaining_s = ns2s(remaining_ns)

        return remaining_s

    @property
    def elapsed(self) -> float:
        # The timer may (and will) overshoot
        # more or less depending on the precision value.
        # Return the duration value in case of an overshoot.
        elapsed_ns = min(self.__elapsed, self.__duration)

        elapsed_s = ns2s(elapsed_ns)

        return elapsed_s

    @property
    def is_complete(self) -> bool:
        is_complete = self.__elapsed >= self.__duration

        return is_complete

    def __adjust(self, delta: float) -> None:
        duration = self.__duration + s2ns(delta)
        self.__validate_duration(duration)
        self.__duration = duration

    @classmethod
    def __validate_number(cls, number: int) -> None:
        if number < 1:
            message = 'Interval numbers are one-based'
            raise InvalidConfigurationError(message)

    @classmethod
    def __validate_duration(cls, duration: float) -> None:
        if duration < 0:
            raise NegativeDurationError
