from aiotimer.interval.twice import twice


def test_twice() -> None:
    generator_factory = twice(42)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [42, 42]
