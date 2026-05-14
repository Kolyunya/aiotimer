from ...error import InvalidDurationError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def sequentially(*durations: float) -> IntervalGeneratorFactory:
    if len(durations) == 0:
        raise InvalidDurationError('Duration sequence must not be empty')

    if any(duration < 0 for duration in durations):
        raise InvalidDurationError

    def factory() -> IntervalGenerator:
        yield from durations

    return factory
