from ..duration import DurationFactory
from .sequentially import sequentially


def thrice(duration: float) -> DurationFactory:
    durations = (duration for _ in range(3))
    interval_factory = sequentially(*durations)

    return interval_factory
