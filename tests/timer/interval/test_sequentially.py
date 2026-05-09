from pytest import raises

from aiotimer.error import InvalidConfigurationError
from aiotimer.interval.sequentially import sequentially


def test_durations_can_not_be_empty() -> None:
    with raises(InvalidConfigurationError) as error:
        sequentially()

    assert str(error.value) == 'Duration sequence must not be empty'


def test_durations_can_not_be_negative() -> None:
    with raises(InvalidConfigurationError) as error:
        sequentially(42, -42, 42)

    assert str(error.value) == 'The duration must be a positive number or zero'


def test_sequentially() -> None:
    generator_factory = sequentially(1, 2, 4, 8, 16)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [1, 2, 4, 8, 16]
