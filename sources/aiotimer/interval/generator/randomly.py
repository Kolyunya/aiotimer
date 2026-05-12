import random

from ...error import InvalidDurationError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def randomly(
    minimum: float,
    maximum: float,
) -> IntervalGeneratorFactory:
    """
    Create a random duration generator generator.

    This function creates an interval generator that yields a single random
    duration between the specified minimum and maximum bounds. Each time a new
    generator is created, it will yield one random value within the range.

    Args:
        minimum: The minimum possible duration in seconds (inclusive).
        maximum: The maximum possible duration in seconds (exclusive).

    Returns:
        An interval generator generator that yields a single random duration.

    Raises:
        InvalidDurationError: If the minimum is greater than or equal
            to the maximum, or if either boundary is not positive.

    Example:
        >>> # Yields a random duration between 3 and 5 seconds.
        >>> randomly(3, 5)

        >>> # Yields a random duration between 0.1 and 0.5 seconds
        >>> randomly(0.1, 0.5)
    """
    if minimum >= maximum:
        raise InvalidDurationError('The minimum duration must be less than the maximum duration')

    if minimum <= 0 or maximum <= 0:
        raise InvalidDurationError('Duration boundaries must be positive')

    def factory() -> IntervalGenerator:
        duration = random.uniform(minimum, maximum)
        yield duration

    return factory
