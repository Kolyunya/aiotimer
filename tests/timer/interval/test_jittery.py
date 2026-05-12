from pytest import approx, raises

from aiotimer.error import InvalidConfigurationError
from aiotimer.interval.generator.jittery import jittery
from aiotimer.interval.generator.once import once
from aiotimer.interval.generator.repeatedly import repeatedly
from aiotimer.interval.generator.thrice import thrice


def test_relative_jitter_can_not_be_negative() -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), relative=-1)

    assert str(error.value) == 'Relative jitter can not be negative'


def test_absolute_jitter_can_not_be_negative() -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), absolute=-1)

    assert str(error.value) == 'Absolute jitter can not be negative'


def test_can_not_specify_two_types_of_jitter() -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), 1, 1)

    assert str(error.value) == 'Exactly one type of jitter must be specified'


def test_can_not_specify_zero_types_of_jitter() -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), None, None)

    assert str(error.value) == 'Exactly one type of jitter must be specified'


def test_jittery_duration_must_be_positive() -> None:
    # Arrange
    factory = jittery(repeatedly(once(1), 100), absolute=2)
    generator = factory()

    # Act
    with raises(InvalidConfigurationError) as error:
        list(generator)

    assert str(error.value) == 'Jittery duration is less than or equals zero'


def test_relative_jitter() -> None:
    interval_factory = repeatedly(once(10), 42)
    generator_factory = jittery(interval_factory, relative=0.1)
    generator = generator_factory()

    intervals = 0
    positive_jitter_generated = False
    negative_jitter_generated = False

    for duration in generator:
        intervals += 1

        if duration > 10:
            positive_jitter_generated = True
        elif duration < 10:
            negative_jitter_generated = True

        assert duration != 10
        assert duration == approx(10, rel=0.1)

    assert intervals == 42
    assert positive_jitter_generated
    assert negative_jitter_generated


def test_absolute_jitter() -> None:
    interval_factory = repeatedly(once(10), 42)
    generator_factory = jittery(interval_factory, absolute=1)
    generator = generator_factory()

    intervals = 0
    positive_jitter_generated = False
    negative_jitter_generated = False

    for duration in generator:
        intervals += 1

        if duration > 10:
            positive_jitter_generated = True
        elif duration < 10:
            negative_jitter_generated = True

        assert duration != 10
        assert duration == approx(10, abs=1)

    assert intervals == 42
    assert positive_jitter_generated
    assert negative_jitter_generated
