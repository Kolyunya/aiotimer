from ..duration import Durations, DurationsFactory


def never() -> DurationsFactory:
    def factory() -> Durations:
        yield from []

    return factory
