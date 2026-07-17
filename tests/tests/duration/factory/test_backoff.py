from pytest import mark, raises

from aiotimer.duration import backoff
from aiotimer.error import InvalidConfigurationError


@mark.parametrize('retries', [-1, 0])
def test_retries_must_be_greater_than_zero(retries: int) -> None:
    with raises(InvalidConfigurationError) as error:
        backoff(retries=retries)

    assert str(error.value) == 'Retries count must be greater than or equal to one'


@mark.parametrize('base', [-1, 0, 1])
def test_base_must_be_greater_than_one(base: int) -> None:
    factory = backoff(retries=3, base=base)

    with raises(InvalidConfigurationError) as error:
        list(factory())

    assert str(error.value) == 'Exponent base must be greater than one'


def test_backoff() -> None:
    factory = backoff(retries=5)

    durations = list(factory())

    assert durations == [0, 1, 2, 4, 8, 16]


def test_faster_growth() -> None:
    factory = backoff(retries=5, base=3.0)

    durations = list(factory())

    assert durations == [0, 1, 3, 9, 27, 81]


def test_scale_down() -> None:
    factory = backoff(retries=5, scale=0.1)

    durations = list(factory())

    assert durations == [0.0, 0.1, 0.2, 0.4, 0.8, 1.6]
