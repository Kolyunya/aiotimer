from itertools import islice

from pytest import raises

from aiotimer.duration.factory import forever, never, sequentially
from aiotimer.error import EmptyDurationIterableError


def test_duration_iterable_must_not_be_empty() -> None:
    # Arrange
    factory = forever(never())
    iterator = iter(factory())

    # Act
    with raises(EmptyDurationIterableError) as error:
        next(iterator)

    # Assert
    assert str(error.value) == 'Duration iterable must not be empty'


def test_forever() -> None:
    # Arrange
    factory = forever(sequentially(1, 2, 3))
    iterator = iter(factory())

    # Act
    durations = list(islice(iterator, 9))

    # Assert
    assert durations == [1, 2, 3, 1, 2, 3, 1, 2, 3]
