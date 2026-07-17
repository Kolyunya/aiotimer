from ..duration import DurationFactory
from .sequentially import sequentially


def twice(duration: float) -> DurationFactory:
    durations = (duration for _ in range(2))
    interval_factory = sequentially(*durations)

    return interval_factory
