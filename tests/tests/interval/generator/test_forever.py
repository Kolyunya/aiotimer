from itertools import islice

from pytest import raises

from aiotimer.error import InvalidConfigurationError
from aiotimer.interval import forever, never, sequentially


def test_durations_generator_must_not_be_degenerate() -> None:
    # Arrange
    factory = forever(never())
    generator = factory()

    # Act
    with raises(InvalidConfigurationError) as error:
        next(generator)

    # Assert
    assert str(error.value) == 'The interval generator must yield at least one value'


def test_forever() -> None:
    # Arrange
    generator_factory = forever(sequentially(1, 2, 3))
    generator = generator_factory()

    # Act
    durations = list(islice(generator, 9))

    # Assert
    assert durations == [1, 2, 3, 1, 2, 3, 1, 2, 3]
