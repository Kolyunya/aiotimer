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
    with raises(InvalidConfigurationError) as error:
        backoff(retries=3, base=base)

    assert str(error.value) == 'Exponent base must be greater than or equal to two'


def test_backoff() -> None:
    factory = backoff(retries=5)

    durations = list(factory())

    assert durations == [0, 1, 2, 4, 8, 16]
