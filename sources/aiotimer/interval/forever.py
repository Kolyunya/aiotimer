from ..error import InvalidConfigurationError
from .type import IntervalGenerator, IntervalGeneratorFactory


def forever(intervals: IntervalGeneratorFactory) -> IntervalGeneratorFactory:
    """
    Create an infinite duration generator factory.

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
                    message = 'Interval generator yielded zero values'
                    raise InvalidConfigurationError(message) from exception

    return factory
