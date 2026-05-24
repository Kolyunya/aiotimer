from ..duration import DurationsFactory
from .sequentially import sequentially


def twice(duration: float) -> DurationsFactory:
    durations = (duration for _ in range(2))
    interval_factory = sequentially(*durations)

    return interval_factory
