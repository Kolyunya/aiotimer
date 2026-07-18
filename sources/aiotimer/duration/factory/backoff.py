from ...error import InvalidConfigurationError
from ..duration import DurationFactory, Durations
from .exponentially import exponentially
from .jittery import jittery


def backoff(
    retries: int,
    base: float = 2.0,
    scale: float = 1.0,
    jitter: float = 0.0,
) -> DurationFactory:
    __validate_retries(retries)

    def factory() -> Durations:
        yield 0.0

        exponentially_factory = exponentially(base, scale=scale, interval_count=retries)
        jittery_factory = jittery(exponentially_factory, relative=jitter)

        retries_iterable = jittery_factory()
        yield from retries_iterable

    return factory


def __validate_retries(retries: int) -> None:
    if retries < 1:
        message = 'Retries count must be greater than or equal to one'
        raise InvalidConfigurationError(message)
