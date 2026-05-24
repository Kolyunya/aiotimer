from aiotimer.duration import twice


def test_twice() -> None:
    factory = twice(42)

    durations = list(factory())

    assert durations == [42, 42]
