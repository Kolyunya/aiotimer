from aiotimer.interval import thrice


def test_thrice() -> None:
    generator_factory = thrice(42)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [42, 42, 42]
