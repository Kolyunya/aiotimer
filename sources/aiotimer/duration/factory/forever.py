from ...error import EmptyDurationIterableError
from ..duration import DurationFactory, DurationIterable, Durations
from ..duration_adapter import DurationAdapter


def forever(durations: Durations) -> DurationFactory:
    adapter = DurationAdapter(durations)

    def factory() -> DurationIterable:
        while True:
            empty_durations = True

            for duration in adapter:
                empty_durations = False
                yield duration

            if empty_durations:
                raise EmptyDurationIterableError

    return factory
