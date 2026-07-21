from pytest import raises

from aiotimer.duration import sequentially
from aiotimer.error import InvalidConfigurationError


def test_durations_can_not_be_empty() -> None:
    with raises(InvalidConfigurationError) as error:
        sequentially()

    assert str(error.value) == 'Durations must not be empty'


def test_durations_can_not_be_negative() -> None:
    with raises(InvalidConfigurationError) as error:
        sequentially(42, -42, 42)

    assert str(error.value) == 'Duration must be a positive number or zero'


def test_sequentially() -> None:
    factory = sequentially(1, 2, 4, 8, 16)

    durations = list(factory())

    assert durations == [1, 2, 4, 8, 16]
