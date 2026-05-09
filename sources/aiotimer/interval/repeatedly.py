from ..error import InvalidConfigurationError
from .type import IntervalGenerator, IntervalGeneratorFactory


def repeatedly(
    generator_factory: IntervalGeneratorFactory,
    count: int,
) -> IntervalGeneratorFactory:
    """
    Create a repeating duration generator factory.

    This function is used as a decorator to repeat another interval generator
    a specified number of times. A generator will yield all durations from the
    decorated generator repeatedly given number of times.

    Args:
        generator_factory: The decorated interval generator factory to repeat.
        count: Number of times to repeat the entire generator sequence.

    Returns:
        An interval generator factory that yields durations repeatedly specified number of times.

    Raises:
        InvalidConfigurationError: If repetitions count is a negative number or zero.

    Example:
        >>> # Yields a 5-second duration 3 times.
        >>> timer = Timer(repeatedly(once(5), 3), on_complete=lambda: print('Done!'))
        >>> await timer.run()

        >>> # Yields the following durations: 1, 2, 3, 1, 2, 3.
        >>> timer = Timer(repeatedly(sequentially(1, 2, 3), 2), on_complete=lambda: print('Done!'))
        >>> await timer.run()

    Note:
        Each repetition creates a fresh generator instance, ensuring that
        the pattern repeats exactly as specified. This is useful for
        creating loops or repeated timing patterns.
    """
    if count <= 0:
        raise InvalidConfigurationError('Repetitions count must be a positive number')

    def factory() -> IntervalGenerator:
        for _ in range(count):
            generator = generator_factory()
            yield from generator

    return factory
