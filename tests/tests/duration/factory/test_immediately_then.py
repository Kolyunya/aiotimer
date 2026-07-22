from aiotimer.duration.factory import immediately_then, once, repeatedly


def test_immediately_then_once() -> None:
    factory = immediately_then(once(42))

    durations = list(factory())

    assert durations == [0, 42]


def test_immediately_then_five_times() -> None:
    factory = immediately_then(repeatedly(once(42), 5))

    durations = list(factory())

    assert durations == [0, 42, 42, 42, 42, 42]
