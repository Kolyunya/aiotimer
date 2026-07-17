from ..duration import DurationFactory
from .sequentially import sequentially


def once(duration: float) -> DurationFactory:
    durations = (duration for _ in range(1))
    interval_factory = sequentially(*durations)

    return interval_factory
