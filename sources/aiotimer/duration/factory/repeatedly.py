from ...error import InvalidConfigurationError
from ..duration import DurationFactory, Durations


def repeatedly(
    durations: DurationFactory,
    count: int,
) -> DurationFactory:
    if count <= 0:
        raise InvalidConfigurationError('Repetitions count must be a positive number')

    def factory() -> Durations:
        for _ in range(count):
            yield from durations()

    return factory
