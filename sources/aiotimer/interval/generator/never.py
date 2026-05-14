from .generator import IntervalGenerator, IntervalGeneratorFactory


def never() -> IntervalGeneratorFactory:
    def factory() -> IntervalGenerator:
        yield from []

    return factory
