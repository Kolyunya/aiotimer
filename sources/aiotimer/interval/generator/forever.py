from ...error import EmptyGeneratorError
from .generator import IntervalGenerator, IntervalGeneratorFactory


def forever(intervals: IntervalGeneratorFactory) -> IntervalGeneratorFactory:
    """
    Create an infinite duration generator generator.

    A generator will act as a decorator and continuously yield
    durations from a decorated generator in an infinite loop.
    """

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
