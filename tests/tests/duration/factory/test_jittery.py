from typing import Optional

from pytest import approx, mark, raises, warns

from aiotimer.duration.factory import jittery, once, repeatedly, thrice
from aiotimer.error import InvalidConfigurationError


def test_relative_jitter_must_be_positive_or_zero() -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), relative=-1)

    assert str(error.value) == 'Relative jitter must be a positive number or zero'


def test_absolute_jitter_must_be_positive_or_zero() -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), absolute=-1)

    assert str(error.value) == 'Absolute jitter must be a positive number or zero'


@mark.parametrize(('relative', 'absolute'), [
    (None, None),
    (1, 1),
])
def test_exactly_one_type_of_jitter_must_be_specified(
    relative: Optional[float],
    absolute: Optional[float],
) -> None:
    with raises(InvalidConfigurationError) as error:
        jittery(thrice(10), relative=relative, absolute=absolute)

    assert str(error.value) == 'Exactly one type of jitter must be specified'


def test_jittery_clamps_negative_durations_to_zero() -> None:
    # Arrange
    factory = jittery(repeatedly(once(1), 100), absolute=2)

    # Act
    with warns(UserWarning, match='A negative duration was clamped to zero'):
        durations = list(factory())

    # Assert
    assert all(duration >= 0 for duration in durations)
    assert any(duration == 0 for duration in durations)


def test_relative_jitter() -> None:
    base_factory = repeatedly(once(10), 42)
    jittery_factory = jittery(base_factory, relative=0.1)

    duration_count = 0
    positive_jitter_generated = False
    negative_jitter_generated = False

    for duration in jittery_factory():
        duration_count += 1

        if duration > 10:
            positive_jitter_generated = True
        elif duration < 10:
            negative_jitter_generated = True

        assert duration != 10
        assert duration == approx(10, rel=0.1)

    assert duration_count == 42
    assert positive_jitter_generated
    assert negative_jitter_generated


def test_absolute_jitter() -> None:
    base_factory = repeatedly(once(10), 42)
    jittery_factory = jittery(base_factory, absolute=1)

    duration_count = 0
    positive_jitter_generated = False
    negative_jitter_generated = False

    for duration in jittery_factory():
        duration_count += 1

        if duration > 10:
            positive_jitter_generated = True
        elif duration < 10:
            negative_jitter_generated = True

        assert duration != 10
        assert duration == approx(10, abs=1)

    assert duration_count == 42
    assert positive_jitter_generated
    assert negative_jitter_generated
