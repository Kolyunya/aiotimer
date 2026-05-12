from ...error import InvalidDurationError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def sequentially(*durations: float) -> IntervalGeneratorFactory:
    """
    Create a sequential duration generator generator.

    Args:
        *durations: Variable number of durations in seconds to execute sequentially.

    Returns:
        An interval generator generator that yields durations in the order provided.

    Raises:
        InvalidDurationError: If no durations are provided or any duration is negative.

    Example:
        >>> # Execute intervals of 1s, 2s, 3s in sequence
        >>> timer = Timer(sequentially(1, 2, 3), on_complete=lambda: print('Done!'))
        >>> await timer.run()

    Note:
        Intervals are executed in the exact order provided. This is useful
        for creating custom timing patterns or multi-stage processes.
    """

    if len(durations) == 0:
        raise InvalidDurationError('Duration sequence must not be empty')

    if any(duration < 0 for duration in durations):
        raise InvalidDurationError

    def factory() -> IntervalGenerator:
        yield from durations

    return factory
