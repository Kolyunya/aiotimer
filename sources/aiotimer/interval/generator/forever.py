from ...error import EmptyGeneratorError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def forever(intervals: IntervalGeneratorFactory) -> IntervalGeneratorFactory:
    def factory() -> IntervalGenerator:
        while True:
            generator = intervals()
            durations = 0

            try:
                while True:
                    duration = next(generator)
                    durations += 1
                    yield duration

            except StopIteration as exception:
                if durations == 0:
                    raise EmptyGeneratorError from exception

    return factory
