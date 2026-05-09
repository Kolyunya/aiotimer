from typing import Optional

from pytest import mark, raises

from aiotimer.error import InvalidConfigurationError
from aiotimer.interval.exponentially import exponentially


@mark.parametrize(('ticks', 'max_duration'), [
    (None, None),
    (10, 60),
])
def test_either_ticks_or_max_duration_must_be_specified(
    ticks: Optional[int],
    max_duration: Optional[float],
) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(1, ticks, max_duration)

    assert str(error.value) == 'Exactly one of intervals count and maximum duration must be specified'


@mark.parametrize('initial_duration', [-1, 0])
def test_initial_duration_must_be_positive(initial_duration: float) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(initial_duration, 10)

    assert str(error.value) == 'Initial duration must be a positive number'


@mark.parametrize('ticks', [-1, 0])
def test_ticks_must_be_positive(ticks: int) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(1, ticks)

    assert str(error.value) == 'Intervals count must be positive'


@mark.parametrize('max_duration', [-1, 0])
def test_max_duration_must_be_positive(max_duration: float) -> None:
    with raises(InvalidConfigurationError) as error:
        exponentially(1, max_duration=max_duration)

    assert str(error.value) == 'Maximum duration must be a positive number'


def test_exponentially_with_ticks_limit() -> None:
    generator_factory = exponentially(1, intervals=5)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [1, 2, 4, 8, 16]


def test_exponentially_with_max_duration_limit() -> None:
    generator_factory = exponentially(1, max_duration=300)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [1, 2, 4, 8, 16, 32, 64, 128, 256]
