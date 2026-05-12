from collections.abc import Callable, Generator

IntervalGenerator = Generator[float, None, None]

IntervalGeneratorFactory = Callable[[], IntervalGenerator]
