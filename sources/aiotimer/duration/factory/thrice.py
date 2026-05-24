from ..duration import DurationsFactory
from .sequentially import sequentially


def thrice(duration: float) -> DurationsFactory:
    durations = (duration for _ in range(3))
    interval_factory = sequentially(*durations)

    return interval_factory
