from ..duration import DurationFactory, Durations


def immediately_then(duration_factory: DurationFactory) -> DurationFactory:
    def factory() -> Durations:
        yield 0

        durations = duration_factory()
        yield from durations

    return factory
