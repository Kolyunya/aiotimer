from .generator import IntervalGenerator, IntervalGeneratorFactory


def immediately_then(then: IntervalGeneratorFactory) -> IntervalGeneratorFactory:
    def factory() -> IntervalGenerator:
        yield 0

        then_generator = then()
        yield from then_generator

    return factory
