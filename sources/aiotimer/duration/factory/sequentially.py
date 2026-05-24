from ...error import InvalidDurationError
from ..duration import Durations, DurationsFactory


def sequentially(*durations: float) -> DurationsFactory:
    if len(durations) == 0:
        raise InvalidDurationError('Duration sequence must not be empty')

    if any(duration < 0 for duration in durations):
        raise InvalidDurationError

    def factory() -> Durations:
        yield from durations

    return factory
