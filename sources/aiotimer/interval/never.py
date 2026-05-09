from .type import IntervalGenerator, IntervalGeneratorFactory


def never() -> IntervalGeneratorFactory:
    """
    Create a degenerate duration generator factory.

    A generator will yield zero durations.
    """

    def factory() -> IntervalGenerator:
        yield from []

    return factory
