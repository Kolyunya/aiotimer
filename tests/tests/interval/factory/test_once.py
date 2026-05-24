from aiotimer.duration import once


def test_once() -> None:
    factory = once(42)

    durations = list(factory())

    assert durations == [42]
