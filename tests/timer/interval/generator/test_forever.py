from itertools import islice

from pytest import raises

from aiotimer.error import InvalidConfigurationError
from aiotimer.interval import sequentially
from aiotimer.interval.generator.forever import forever
from aiotimer.interval.generator.never import never


def test_durations_generator_must_not_be_degenerate() -> None:
    # Arrange
    factory = forever(never())
    generator = factory()

    # Act
    with raises(InvalidConfigurationError) as error:
        next(generator)

    # Assert
    assert str(error.value) == 'The interval generator yielded no values'


def test_forever() -> None:
    # Arrange
    generator_factory = forever(sequentially(1, 2, 3))
    generator = generator_factory()

    # Act
    durations = list(islice(generator, 9))

    # Assert
    assert durations == [1, 2, 3, 1, 2, 3, 1, 2, 3]
