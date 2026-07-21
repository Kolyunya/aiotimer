from ..duration import DurationFactory, Durations
from .repeatedly import repeatedly


def once(durations: Durations) -> DurationFactory:
    factory = repeatedly(durations, 1)

    return factory
