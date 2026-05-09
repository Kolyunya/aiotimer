import random
from typing import Optional

from ..error import InvalidConfigurationError
from ..utility.boolean import coin_flip
from .type import IntervalGenerator, IntervalGeneratorFactory


def jittery(
    generator_factory: IntervalGeneratorFactory,
    relative: Optional[float] = None,
    absolute: Optional[float] = None,
) -> IntervalGeneratorFactory:
    """
    Create a jittery duration generator factory.

    This function is used as a decorator to add random jitter to other
    interval generators. A generator will yield durations with random jitter
    applied to each duration from the provided generator factory. The jitter can
    be specified either as a relative percentage of the original duration or
    as an absolute value.

    Args:
        generator_factory: The base interval generator factory to apply jitter to.
        relative: Optional relative jitter as a fraction of the duration (e.g., 0.1 for ±10%).
        absolute: Optional absolute jitter value in seconds (e.g., 0.5 for ±0.5 seconds).

    Returns:
        An interval generator factory that yields durations with applied jitter.

    Raises:
        InvalidConfigurationError: If both relative and absolute are specified,
            if neither is specified, if either value is negative, or if the
            resulting jittery duration is less than or equal to zero.

    Example:
        >>> # ±10% relative jitter.
        >>> jittery(once(5), relative=0.1)  # Yields value between 4.5 and 5.5

        >>> # ±0.5 seconds absolute jitter.
        >>> jittery(once(5), absolute=0.5)  # Yields value between 4.5 and 5.5
    """

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

    def factory() -> IntervalGenerator:
        generator = generator_factory()

        for duration in generator:
            multiplier = 1 if coin_flip() else -1

            if relative is not None:
                jitter_threshold = duration * relative
            elif absolute is not None:
                jitter_threshold = absolute
            else:
                raise InvalidConfigurationError('Exactly only type of jitter must be specified')

            the_jitter = random.uniform(0, jitter_threshold) * multiplier
            jittery_duration = duration + the_jitter

            if jittery_duration <= 0:
                raise InvalidConfigurationError('Jittery duration is less than or equals zero')

            yield jittery_duration

    return factory
