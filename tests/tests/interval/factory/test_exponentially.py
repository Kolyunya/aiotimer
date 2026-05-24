from typing import Optional

from pytest import mark, raises

from aiotimer.duration import exponentially
from aiotimer.error import InvalidConfigurationError


@mark.parametrize(('interval_count', 'maximum_duration'), [
    (None, None),
    (10, 60),
])
def test_exactly_one_of_interval_count_or_maximum_duration_must_be_specified(
    interval_count: Optional[int],
    maximum_duration: Optional[float],
) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(
            interval_count=interval_count,
            maximum_duration=maximum_duration,
        )

    assert str(error.value) == 'Exactly one of `interval_count` and `maximum_duration` must be specified'


@mark.parametrize('base', [-1, 0, 1])
def test_base_must_be_greater_than_one(base: int) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(base, interval_count=10)

    assert str(error.value) == 'Exponent base must be greater than one'


@mark.parametrize('interval_count', [-1, 0, 1])
def test_interval_count_must_be_greater_than_one(interval_count: int) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(interval_count=interval_count)

    assert str(error.value) == 'Interval count must be greater than one'


@mark.parametrize('maximum_duration', [-1, 0, 1])
def test_maximum_duration_must_be_greater_than_one(maximum_duration: float) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(maximum_duration=maximum_duration)

    assert str(error.value) == 'Maximum duration must be greater than one'


def test_exponentially_with_interval_count() -> None:
    factory = exponentially(interval_count=5)

    durations = list(factory())

    assert durations == [1, 2, 4, 8, 16]


def test_exponentially_with_maximum_duration() -> None:
    factory = exponentially(maximum_duration=300)

    durations = list(factory())

    assert durations == [1, 2, 4, 8, 16, 32, 64, 128, 256]
