from .generator import IntervalGeneratorFactory
from .sequentially import sequentially


def thrice(duration: float) -> IntervalGeneratorFactory:
    """
    Create a triple duration generator generator.

    A generator will yield three durations, each of `duration` seconds.
    """

    durations = (duration for _ in range(3))
    interval_factory = sequentially(*durations)

    return interval_factory
