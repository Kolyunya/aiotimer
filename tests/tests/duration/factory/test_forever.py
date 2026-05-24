from itertools import islice

from pytest import raises

from aiotimer.duration import forever, never, sequentially
from aiotimer.error import EmptyDurationIterableError


def test_durations_generator_must_not_be_degenerate() -> None:
    # Arrange
    factory = forever(never())
    iterator = iter(factory())

    # Act
    with raises(EmptyDurationIterableError) as error:
        next(iterator)

    # Assert
    assert str(error.value) == 'Duration iterable must have at least one value'


def test_forever() -> None:
    # Arrange
    factory = forever(sequentially(1, 2, 3))
    iterator = iter(factory())

    # Act
    durations = list(islice(iterator, 9))

    # Assert
    assert durations == [1, 2, 3, 1, 2, 3, 1, 2, 3]
