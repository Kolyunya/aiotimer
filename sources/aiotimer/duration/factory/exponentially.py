from typing import Optional

from ...error import InvalidConfigurationError, InvalidDurationError
from ..duration import DurationFactory, Durations


def exponentially(
    base: float = 2.0,
    scale: float = 1.0,
    interval_count: Optional[int] = None,
    maximum_duration: Optional[float] = None,
) -> DurationFactory:
    __validate_base(base)
    __validate_scale(scale)
    __validate_limits(interval_count, maximum_duration)

    def factory() -> Durations:
        interval_numer = 0

        while True:
            duration = pow(base, interval_numer) * scale
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


def __validate_base(base: float) -> None:
    if base <= 1:
        raise InvalidConfigurationError('Exponent base must be greater than one')


def __validate_scale(scale: float) -> None:
    if scale <= 0:
        raise InvalidConfigurationError('Exponent scale must be greater than zero')


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

    if interval_count is not None and interval_count <= 0:
        raise InvalidConfigurationError('Interval count must be greater than zero')

    if maximum_duration is not None and maximum_duration <= 0:
        raise InvalidDurationError('Maximum duration must be greater than zero')
