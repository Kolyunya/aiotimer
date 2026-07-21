from ..duration import DurationFactory, Durations
from .repeatedly import repeatedly


def thrice(durations: Durations) -> DurationFactory:
    factory = repeatedly(durations, 3)

    return factory
