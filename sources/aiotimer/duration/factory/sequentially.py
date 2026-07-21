from ...error import InvalidConfigurationError
from ..duration import DurationFactory, DurationIterable, Durations
from ..duration_adapter import DurationAdapter


def sequentially(*durations: Durations) -> DurationFactory:
    if len(durations) == 0:
        raise InvalidConfigurationError('Durations must not be empty')

    adapters = [
        DurationAdapter(durations_item)
        for durations_item in durations
    ]

    def factory() -> DurationIterable:
        for adapter in adapters:
            yield from adapter

    return factory
