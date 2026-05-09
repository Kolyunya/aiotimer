from typing import Optional

from ..error import InvalidConfigurationError, InvalidDurationError
from .type import IntervalGenerator, IntervalGeneratorFactory


def exponentially(
    initial_duration: float = 1,
    intervals: Optional[int] = None,
    max_duration: Optional[float] = None,
) -> IntervalGeneratorFactory:
    """
    Create an exponential duration generator factory.

    A generator will sequentially yield factors of two
    multiplied by the initial value.
    E.g., with an initial duration of 1, a generator
    would yield the following durations: 1, 2, 4, 8, 16, etc.
    The number of produced durations may be flexibly controlled
    via the fixed interval count or via the maximum value of
    the duration.
    """

    if initial_duration <= 0:
        raise InvalidDurationError('Initial duration must be a positive number')

    if (
        (intervals is None and max_duration is None)
        or
        (intervals is not None and max_duration is not None)
    ):
        message = 'Exactly one of intervals count and maximum duration must be specified'
        raise InvalidConfigurationError(message)

    if intervals is not None and intervals < 1:
        raise InvalidConfigurationError('Intervals count must be positive')

    if max_duration is not None and max_duration < 1:
        raise InvalidDurationError('Maximum duration must be a positive number')

    def factory() -> IntervalGenerator:
        tick = 0

        while True:
            duration = initial_duration * pow(2, tick)
            tick += 1

            if (
                (intervals is not None and intervals >= tick)
                or
                (max_duration is not None and max_duration >= duration)
            ):
                yield duration
            else:
                break

    return factory
