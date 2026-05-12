from time import monotonic
from typing import Optional

from ..error import InvalidConfigurationError, InvalidDurationError


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

        self.__advanced_at: Optional[float] = None
        self.__elapsed: float = 0

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

    def prolong(self, delta: float) -> None:
        self.__adjust(delta)

    def shorten(self, delta: float) -> None:
        self.__adjust(-1 * delta)

    @property
    def is_complete(self) -> bool:
        result = self.__elapsed >= self.__duration

        return result

    @property
    def time_left(self) -> float:
        result = self.__duration - self.__elapsed

        # The timer may (and will) overshoot more or less
        # depending on the duration-to-precision ratio.
        # Return zero in case of an overshoot.
        result = max(result, 0)

        return result

    def advance(self) -> None:
        now = monotonic()

        # `self.__advanced_at` is `None` on the first iteration
        # of the advancement cycle.
        if self.__advanced_at is not None:
            elapsed = now - self.__advanced_at
            self.__elapsed += elapsed

        self.__advanced_at = now

    def stop_advancement(self) -> None:
        self.__advanced_at = None

    def __adjust(self, delta: float) -> None:
        duration = self.__duration + delta
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
            raise InvalidDurationError
