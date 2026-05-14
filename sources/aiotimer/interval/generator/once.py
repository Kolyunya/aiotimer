from .generator import IntervalGeneratorFactory
from .sequentially import sequentially


def once(duration: float) -> IntervalGeneratorFactory:
    durations = (duration for _ in range(1))
    interval_factory = sequentially(*durations)

    return interval_factory
