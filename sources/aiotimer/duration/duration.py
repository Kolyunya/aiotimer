from collections.abc import Callable, Iterable

Durations = Iterable[float]

DurationFactory = Callable[[], Durations]
