from .generator import IntervalGenerator, IntervalGeneratorFactory


def never() -> IntervalGeneratorFactory:
    """
    Create a degenerate duration generator generator.

    A generator will yield zero durations.
    """

    def factory() -> IntervalGenerator:
        yield from []

    return factory
