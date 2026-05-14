from .generator import IntervalGeneratorFactory
from .sequentially import sequentially


def thrice(duration: float) -> IntervalGeneratorFactory:
    durations = (duration for _ in range(3))
    interval_factory = sequentially(*durations)

    return interval_factory
