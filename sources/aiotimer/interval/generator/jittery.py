import random
from typing import Optional

from ...error import InvalidConfigurationError
from ...utility.boolean import coin_flip
from .generator import IntervalGenerator, IntervalGeneratorFactory


def jittery(
    generator_factory: IntervalGeneratorFactory,
    relative: Optional[float] = None,
    absolute: Optional[float] = None,
) -> IntervalGeneratorFactory:
    __validate_jitter(relative, absolute)

    def factory() -> IntervalGenerator:
        generator = generator_factory()

        for duration in generator:
            multiplier = 1 if coin_flip() else -1

            if relative is not None:
                jitter_threshold = duration * relative
            elif absolute is not None:
                jitter_threshold = absolute
            else:
                raise InvalidConfigurationError('Exactly one type of jitter must be specified')

            the_jitter = random.uniform(0, jitter_threshold) * multiplier
            jittery_duration = duration + the_jitter

            if jittery_duration <= 0:
                raise InvalidConfigurationError('Jittery duration is less than or equals zero')

            yield jittery_duration

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
        raise InvalidConfigurationError('Relative jitter can not be negative')

    if absolute is not None and absolute < 0:
        raise InvalidConfigurationError('Absolute jitter can not be negative')
