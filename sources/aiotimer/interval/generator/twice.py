from .generator import IntervalGeneratorFactory
from .sequentially import sequentially


def twice(duration: float) -> IntervalGeneratorFactory:
    durations = (duration for _ in range(2))
    interval_factory = sequentially(*durations)

    return interval_factory
