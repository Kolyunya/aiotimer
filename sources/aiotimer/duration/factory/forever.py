from ...error import EmptyDurationIterableError
from ..duration import Durations, DurationsFactory


def forever(durations: DurationsFactory) -> DurationsFactory:
    def factory() -> Durations:
        while True:
            duration_iterator = iter(durations())
            duration_count = 0

            try:
                while True:
                    duration = next(duration_iterator)
                    duration_count += 1
                    yield duration

            except StopIteration as exception:
                if duration_count == 0:
                    raise EmptyDurationIterableError from exception

    return factory
