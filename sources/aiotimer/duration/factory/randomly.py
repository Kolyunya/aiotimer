import random

from ...error import NegativeDurationError
from ..duration import DurationFactory, Durations


def randomly(
    minimum: float,
    maximum: float,
) -> DurationFactory:
    if minimum >= maximum:
        raise NegativeDurationError('The minimum duration must be less than the maximum duration')

    if minimum <= 0 or maximum <= 0:
        raise NegativeDurationError('Duration boundaries must be positive')

    def factory() -> Durations:
        duration = random.uniform(minimum, maximum)
        yield duration

    return factory
