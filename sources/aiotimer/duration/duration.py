from collections.abc import Callable, Iterable

Durations = Iterable[float]

DurationsFactory = Callable[[], Durations]
