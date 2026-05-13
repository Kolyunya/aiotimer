from aiotimer.interval.generator.once import once


def test_once() -> None:
    generator_factory = once(42)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [42]
