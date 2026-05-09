from .sequentially import sequentially
from .type import IntervalGeneratorFactory


def thrice(duration: float) -> IntervalGeneratorFactory:
    """
    Create a triple duration generator factory.

    A generator will yield three durations, each of `duration` seconds.
    """

    durations = (duration for _ in range(3))
    interval_factory = sequentially(*durations)

    return interval_factory
