from ...error import InvalidConfigurationError
from ..duration import DurationFactory, Durations
from .exponentially import exponentially


def backoff(retries: int, base: float = 2.0, scale: float = 1.0) -> DurationFactory:
    __validate_retries(retries)

    def factory() -> Durations:
        yield 0.0

        retries_factory = exponentially(base, scale, interval_count=retries)
        retries_iterable = retries_factory()
        yield from retries_iterable

    return factory


def __validate_retries(retries: int) -> None:
    if retries < 1:
        message = 'Retries count must be greater than or equal to one'
        raise InvalidConfigurationError(message)
