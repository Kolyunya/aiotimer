from .generator import IntervalGeneratorFactory
from .sequentially import sequentially


def twice(duration: float) -> IntervalGeneratorFactory:
    """
    Create a double duration generator generator.

    A generator will yield two durations, each of `duration` seconds.
    """

    durations = (duration for _ in range(2))
    interval_factory = sequentially(*durations)

    return interval_factory
