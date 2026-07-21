from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Union

Duration = Union[float, int]
DurationSequence = Sequence[Duration]
DurationIterator = Iterator[Duration]
DurationIterable = Iterable[Duration]
DurationFactory = Callable[[], DurationIterable]
Durations = Union[Duration, DurationSequence, DurationFactory]
