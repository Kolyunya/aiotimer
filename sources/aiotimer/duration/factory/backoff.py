from ...error import InvalidConfigurationError, NegativeDurationError
from ..duration import DurationFactory, Durations
from .exponentially import exponentially


def backoff(retries: int, base: int = 2) -> DurationFactory:
    __validate_retries(retries)
    __validate_base(base)

    def factory() -> Durations:
        yield 0.0

        retries_factory = exponentially(base, retries)
        retries_iterable = retries_factory()
        yield from retries_iterable

    return factory


def __validate_retries(retries: int) -> None:
    if retries < 1:
        message = 'Retries count must be greater than or equal to one'
        raise InvalidConfigurationError(message)


def __validate_base(base: int) -> None:
    if base < 2:
        message = 'Exponent base must be greater than or equal to two'
        raise NegativeDurationError(message)
