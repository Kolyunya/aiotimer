from .sequentially import sequentially
from .type import IntervalGeneratorFactory


def once(duration: float) -> IntervalGeneratorFactory:
    """
    Create a single duration generator factory.

    Args:
        duration: The duration in seconds for the single interval.

    Returns:
        An interval generator factory that yields exactly one duration.

    Example:
        >>> # Create a 5-second-long single interval
        >>> timer = Timer(once(5), on_complete=lambda: print('Done!'))
        >>> await timer.run()

    Note:
        This is the simplest interval pattern, useful for one-shot timers
        or as building blocks for more complex patterns.
    """

    durations = (duration for _ in range(1))
    interval_factory = sequentially(*durations)

    return interval_factory
