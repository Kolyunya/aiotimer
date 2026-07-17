from pytest import mark, raises

from aiotimer.duration import once, repeatedly, sequentially
from aiotimer.error import InvalidConfigurationError


@mark.parametrize('count', [-1, 0])
def test_repetitions_count_must_be_positive(count: int) -> None:
    with raises(InvalidConfigurationError) as error:
        repeatedly(once(42), count)

    assert str(error.value) == 'Repetitions count must be a positive number'


def test_single_repetition() -> None:
    factory = repeatedly(once(42), 3)

    durations = list(factory())

    assert durations == [42, 42, 42]


def test_pattern_repetition() -> None:
    factory = repeatedly(sequentially(1, 2, 3), 3)

    durations = list(factory())

    assert durations == [1, 2, 3,   1, 2, 3,   1, 2, 3]
