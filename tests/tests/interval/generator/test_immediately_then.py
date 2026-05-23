from aiotimer.interval import immediately_then, once, repeatedly


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
