import random

from ...error import InvalidDurationError
from ..duration import DurationFactory, Durations


def randomly(
    minimum: float,
    maximum: float,
) -> DurationFactory:
    if minimum >= maximum:
        raise InvalidDurationError('The minimum duration must be less than the maximum duration')

    if minimum <= 0 or maximum <= 0:
        raise InvalidDurationError('Duration boundaries must be positive')

    def factory() -> Durations:
        duration = random.uniform(minimum, maximum)
        yield duration

    return factory
