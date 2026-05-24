from ..duration import Durations, DurationsFactory


def immediately_then(durations: DurationsFactory) -> DurationsFactory:
    def factory() -> Durations:
        yield 0

        then_generator = durations()
        yield from then_generator

    return factory
