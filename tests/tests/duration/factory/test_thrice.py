from aiotimer.duration import thrice


def test_thrice() -> None:
    factory = thrice(42)

    durations = list(factory())

    assert durations == [42, 42, 42]
