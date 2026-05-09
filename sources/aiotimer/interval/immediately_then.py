from .type import IntervalGenerator, IntervalGeneratorFactory


def immediately_then(then: IntervalGeneratorFactory) -> IntervalGeneratorFactory:
    """
    Create an instant duration generator factory.

    A generator will act as a decorator for another generator.
    It will initially yield a zero-second duration and then
    yield durations from a decorated generator.
    Use this factory when you need the first interval
    to complete immediately.
    """

    def factory() -> IntervalGenerator:
        yield 0

        then_generator = then()
        yield from then_generator

    return factory
