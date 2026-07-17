from ..duration import DurationFactory, Durations


def never() -> DurationFactory:
    def factory() -> Durations:
        yield from []

    return factory
