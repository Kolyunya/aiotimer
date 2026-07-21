from ...error import InvalidConfigurationError
from ..duration import DurationFactory, DurationIterable, Durations
from ..duration_adapter import DurationAdapter


def repeatedly(durations: Durations, count: int) -> DurationFactory:
    if count <= 0:
        raise InvalidConfigurationError('Repetitions count must be a positive number')

    adapter = DurationAdapter(durations)

    def factory() -> DurationIterable:
        for _iteration in range(count):
            yield from adapter

    return factory
