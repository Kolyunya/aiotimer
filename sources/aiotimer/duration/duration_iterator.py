from collections.abc import Callable, Iterable, Iterator
from typing import Union, cast

from typing_extensions import override

from aiotimer.error import InvalidDurationError

SingleDuration = float
MultipleDurations = list[SingleDuration]
DurationsFactory = Callable[[], Iterable[SingleDuration]]
Durations = Union[SingleDuration, MultipleDurations, DurationsFactory]


class DurationIterator(Iterable[float]):

    def __init__(self, durations: Durations) -> None:
        self.__durations: Durations = durations

        if isinstance(durations, (float, int)):
            self.__iterator_factory = self.__from_single_duration
        elif isinstance(durations, list):
            self.__iterator_factory = self.__from_durations_list
        elif callable(durations):
            self.__iterator_factory = self.__from_durations_factory
        else:
            raise InvalidDurationError

    @override
    def __iter__(self) -> Iterator[float]:
        iterator = self.__iterator_factory()

        return iterator

    def __from_single_duration(self) -> Iterator[SingleDuration]:
        duration = cast('SingleDuration', self.__durations)
        durations = [duration]
        iterator = iter(durations)

        return iterator

    def __from_durations_list(self) -> Iterator[SingleDuration]:
        durations = cast('MultipleDurations', self.__durations)
        iterator = iter(durations)

        return iterator

    def __from_durations_factory(self) -> Iterator[SingleDuration]:
        factory = cast('DurationsFactory', self.__durations)
        iterable = factory()
        iterator = iter(iterable)

        return iterator
