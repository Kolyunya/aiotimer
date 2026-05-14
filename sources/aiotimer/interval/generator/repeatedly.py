from ...error import InvalidConfigurationError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def repeatedly(
    generator_factory: IntervalGeneratorFactory,
    count: int,
) -> IntervalGeneratorFactory:
    if count <= 0:
        raise InvalidConfigurationError('Repetitions count must be a positive number')

    def factory() -> IntervalGenerator:
        for _ in range(count):
            generator = generator_factory()
            yield from generator

    return factory
