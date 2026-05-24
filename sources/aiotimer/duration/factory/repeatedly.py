from ...error import InvalidConfigurationError
from ..duration import Durations, DurationsFactory


def repeatedly(
    durations: DurationsFactory,
    count: int,
) -> DurationsFactory:
    if count <= 0:
        raise InvalidConfigurationError('Repetitions count must be a positive number')

    def factory() -> Durations:
        for _ in range(count):
            yield from durations()

    return factory
