from pytest import mark, raises

from aiotimer.error import InvalidConfigurationError
from aiotimer.interval.generator.once import once
from aiotimer.interval.generator.repeatedly import repeatedly
from aiotimer.interval.generator.sequentially import sequentially


@mark.parametrize('count', [-1, 0])
def test_repetitions_count_must_be_positive(count: int) -> None:
    with raises(InvalidConfigurationError) as error:
        repeatedly(once(42), count)

    assert str(error.value) == 'Repetitions count must be a positive number'


def test_single_repetition() -> None:
    generator_factory = repeatedly(once(42), 3)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [42, 42, 42]


def test_pattern_repetition() -> None:
    generator_factory = repeatedly(sequentially(1, 2, 3), 3)
    generator = generator_factory()

    durations = list(generator)

    assert durations == [1, 2, 3,   1, 2, 3,   1, 2, 3]
