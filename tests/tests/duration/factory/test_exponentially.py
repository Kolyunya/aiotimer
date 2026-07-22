from typing import Optional

from pytest import mark, raises

from aiotimer.duration.factory import exponentially
from aiotimer.error import InvalidConfigurationError, InvalidDurationError


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
def test_base_must_be_greater_than_one(base: float) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(base, interval_count=10)

    assert str(error.value) == 'Exponent base must be greater than one'


@mark.parametrize('scale', [-1, 0])
def test_scale_must_be_greater_than_zero(scale: float) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(scale=scale, interval_count=10)

    assert str(error.value) == 'Exponent scale must be greater than zero'


@mark.parametrize('interval_count', [-1, 0])
def test_interval_count_must_be_greater_than_zero(interval_count: int) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(interval_count=interval_count)

    assert str(error.value) == 'Interval count must be greater than zero'


@mark.parametrize('maximum_duration', [-1, 0])
def test_maximum_duration_must_be_greater_than_zero(maximum_duration: float) -> None:
    with raises(InvalidDurationError) as error:
        exponentially(maximum_duration=maximum_duration)

    assert str(error.value) == 'Maximum duration must be greater than zero'


def test_interval_count_limit() -> None:
    factory = exponentially(interval_count=5)

    durations = list(factory())

    assert durations == [1, 2, 4, 8, 16]


@mark.parametrize('maximum_duration', [16, 31.999])
def test_maximum_duration_limit(maximum_duration: float) -> None:
    factory = exponentially(maximum_duration=maximum_duration)

    durations = list(factory())

    assert durations == [1, 2, 4, 8, 16]


def test_slower_growth() -> None:
    factory = exponentially(1.5, interval_count=3)

    durations = list(factory())

    assert durations == [1, 1.5, 2.25]


def test_faster_growth() -> None:
    factory = exponentially(3.0, interval_count=3)

    durations = list(factory())

    assert durations == [1, 3, 9]


def test_scale_down() -> None:
    factory = exponentially(scale=0.1, interval_count=3)

    durations = list(factory())

    assert durations == [0.1, 0.2, 0.4]


def test_scale_up() -> None:
    factory = exponentially(scale=10.0, interval_count=3)

    durations = list(factory())

    assert durations == [10, 20, 40]
