from ..duration import DurationFactory
from .sequentially import sequentially


def once(duration: float) -> DurationFactory:
    interval_factory = sequentially(duration)

    return interval_factory
