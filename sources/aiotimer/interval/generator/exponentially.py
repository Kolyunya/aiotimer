from typing import Optional

from ...error import InvalidConfigurationError, InvalidDurationError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def exponentially(
    base: int = 2,
    interval_count: Optional[int] = None,
    maximum_duration: Optional[float] = None,
) -> IntervalGeneratorFactory:
    __validate_base(base)
    __validate_limits(interval_count, maximum_duration)

    def factory() -> IntervalGenerator:
        interval_numer = 0

        while True:
            duration = pow(base, interval_numer)
            interval_numer += 1

            if (
                (interval_count is not None and interval_count >= interval_numer)
                or
                (maximum_duration is not None and maximum_duration >= duration)
            ):
                yield duration
            else:
                break

    return factory


def __validate_base(base: int) -> None:
    if base <= 1:
        raise InvalidDurationError('Exponent base must be greater than one')


def __validate_limits(
    interval_count: Optional[int],
    maximum_duration: Optional[float],
) -> None:
    if (
        (interval_count is None and maximum_duration is None)
        or
        (interval_count is not None and maximum_duration is not None)
    ):
        message = 'Exactly one of `interval_count` and `maximum_duration` must be specified'
        raise InvalidConfigurationError(message)

    if interval_count is not None and interval_count <= 1:
        raise InvalidConfigurationError('Interval count must be greater than one')

    if maximum_duration is not None and maximum_duration <= 1:
        raise InvalidDurationError('Maximum duration must be greater than one')
