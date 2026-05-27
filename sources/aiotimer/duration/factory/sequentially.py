from ...error import NegativeDurationError
from ..duration import Durations, DurationsFactory


def sequentially(*durations: float) -> DurationsFactory:
    if len(durations) == 0:
        raise NegativeDurationError('Duration sequence must not be empty')

    if any(duration < 0 for duration in durations):
        raise NegativeDurationError

    def factory() -> Durations:
        yield from durations

    return factory
