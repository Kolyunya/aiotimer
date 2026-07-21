from typing import Optional

from ...error import InvalidConfigurationError, InvalidDurationError
from ..duration import DurationFactory
from .exponentially import exponentially
from .immediately_then import immediately_then
from .jittery import jittery


def backoff(
    retries: Optional[int] = None,
    maximum_duration: Optional[float] = None,
    base: float = 2.00,
    scale: float = 0.50,
    jitter: float = 0.25,
) -> DurationFactory:
    __validate_limits(retries, maximum_duration)

    if retries is None and maximum_duration is None:
        retries = 5

    _exponentially = exponentially(base, scale, retries, maximum_duration)
    _jittery = jittery(_exponentially, jitter)
    _backoff = immediately_then(_jittery)

    return _backoff


def __validate_limits(
    retries: Optional[int],
    maximum_duration: Optional[float],
) -> None:
    if retries is not None and maximum_duration is not None:
        message = 'Only one of `retries` and `maximum_duration` may be specified'
        raise InvalidConfigurationError(message)

    if retries is not None and retries <= 0:
        raise InvalidConfigurationError('Retries count must be greater than zero')

    if maximum_duration is not None and maximum_duration <= 0:
        raise InvalidDurationError('Maximum duration must be greater than zero')
