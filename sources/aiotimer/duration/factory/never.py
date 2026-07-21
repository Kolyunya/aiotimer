from ..duration import DurationFactory, DurationIterable


def never() -> DurationFactory:
    def factory() -> DurationIterable:
        yield from []

    return factory
