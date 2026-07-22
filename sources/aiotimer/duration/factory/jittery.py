import random
from typing import Optional
from warnings import warn

from ...error import InvalidConfigurationError, LogicError
from ..duration import DurationFactory, DurationIterable, Durations
from ..duration_adapter import DurationAdapter


def jittery(
    durations: Durations,
    relative: Optional[float] = None,
    absolute: Optional[float] = None,
) -> DurationFactory:
    __validate_jitter(relative, absolute)

    adapter = DurationAdapter(durations)

    def factory() -> DurationIterable:
        for duration in adapter:

            if relative is not None:
                maximum_jitter = duration * relative
            elif absolute is not None:
                maximum_jitter = absolute
            else:
                raise LogicError('Either `relative` or `absolute` is guaranteed to be specified')

            jitter = random.uniform(-1 * maximum_jitter, maximum_jitter)
            jittered_duration = duration + jitter

            if jittered_duration < 0:
                jittered_duration = 0

                warning = 'A negative duration was clamped to zero.'
                warn(warning, stacklevel=2)

            yield jittered_duration

    return factory


def __validate_jitter(
    relative: Optional[float],
    absolute: Optional[float],
) -> None:
    if (
        (relative is not None and absolute is not None)
        or
        (relative is None and absolute is None)
    ):
        raise InvalidConfigurationError('Exactly one type of jitter must be specified')

    if relative is not None and relative < 0:
        raise InvalidConfigurationError('Relative jitter must be a positive number or zero')

    if absolute is not None and absolute < 0:
        raise InvalidConfigurationError('Absolute jitter must be a positive number or zero')
