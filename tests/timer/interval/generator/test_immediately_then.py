from aiotimer.interval.generator.immediately_then import immediately_then
from aiotimer.interval.generator.once import once
from aiotimer.interval.generator.repeatedly import repeatedly


def test_immediately_then_once() -> None:
    generator_factory = immediately_then(once(42))
    generator = generator_factory()

    durations = list(generator)

    assert durations == [0, 42]


def test_immediately_then_five_times() -> None:
    generator_factory = immediately_then(repeatedly(once(42), 5))
    generator = generator_factory()

    durations = list(generator)

    assert durations == [0, 42, 42, 42, 42, 42]
