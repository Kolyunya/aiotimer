from collections.abc import Callable, Sequence

from typing_extensions import override

from ..error import (
    EmptyDurationIterableError,
    InvalidDurationError,
    NegativeDurationError,
)
from .duration import (
    Duration,
    DurationFactory,
    DurationIterable,
    DurationIterator,
    Durations,
    DurationSequence,
)


class DurationAdapter(DurationIterable):

    def __init__(self, durations: Durations) -> None:
        self.__duration_factory: DurationFactory

        # Replace with the following line after support for Python 3.9 is dropped.
        # if isinstance(durations, Duration):
        if isinstance(durations, (float, int)):
            duration: Duration = durations
            self.__duration_factory = self.__duration_to_factory(duration)

        elif isinstance(durations, Sequence):
            sequence: DurationSequence = durations  # ty: ignore[invalid-assignment]  # pyright: ignore[reportUnknownVariableType]
            self.__duration_factory = self.__sequence_to_factory(sequence)

        elif isinstance(durations, Callable):  # type: ignore[arg-type]  # pyright: ignore[reportUnnecessaryIsInstance]
            self.__duration_factory = durations

        else:
            raise InvalidDurationError

    @override
    def __iter__(self) -> DurationIterator:
        iterable = self.__duration_factory()
        iterator = iter(iterable)

        return iterator

    def __duration_to_factory(self, duration: Duration) -> DurationFactory:
        self.__validate_duration(duration)

        def factory() -> DurationIterable:
            iterable = [duration]
            return iterable

        return factory

    def __sequence_to_factory(self, sequence: DurationSequence) -> DurationFactory:
        self.__validate_sequence(sequence)

        def factory() -> DurationIterable:
            return sequence

        return factory

    def __validate_duration(self, duration: Duration) -> None:
        if duration < 0:
            raise NegativeDurationError

    def __validate_sequence(self, sequence: DurationSequence) -> None:
        if len(sequence) == 0:
            raise EmptyDurationIterableError

        for duration in sequence:
            self.__validate_duration(duration)
