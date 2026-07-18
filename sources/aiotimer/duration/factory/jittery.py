import random
from typing import Optional
from warnings import warn

from ...error import InvalidConfigurationError, LogicError
from ..duration import DurationFactory, Durations


def jittery(
    durations: DurationFactory,
    relative: Optional[float] = None,
    absolute: Optional[float] = None,
) -> DurationFactory:
    __validate_jitter(relative, absolute)
    assert relative is not None or absolute is not None

    def factory() -> Durations:
        for duration in durations():

            if relative is not None:
                maximum_jitter = duration * relative
            elif absolute is not None:
                maximum_jitter = absolute
            else:
                raise LogicError('Either `relative` or `absolute` is guaranteed to be specified')

            assert relative is not None or absolute is not None
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
        raise InvalidConfigurationError('Relative jitter must not be negative')

    if absolute is not None and absolute < 0:
        raise InvalidConfigurationError('Absolute jitter must not be negative')
