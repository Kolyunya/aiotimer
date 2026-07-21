from ..duration import DurationFactory, Durations
from .repeatedly import repeatedly


def twice(durations: Durations) -> DurationFactory:
    factory = repeatedly(durations, 2)

    return factory
