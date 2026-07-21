from ..duration import DurationFactory, Durations
from .sequentially import sequentially


def immediately_then(durations: Durations) -> DurationFactory:
    factory = sequentially(0, durations)

    return factory
