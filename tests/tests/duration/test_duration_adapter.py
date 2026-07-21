from pytest import mark, raises

from aiotimer.duration import (
    Duration,
    DurationAdapter,
    DurationFactory,
    Durations,
    DurationSequence,
)
from aiotimer.duration.factory import sequentially
from aiotimer.error import EmptyDurationIterableError, NegativeDurationError


@mark.parametrize('duration', [42.0, 42])
def test_construct_from_single_duration(duration: Duration) -> None:
    adapter = DurationAdapter(42)

    durations = list(adapter)

    assert durations == [duration]


@mark.parametrize('duration', [42.0, 42])
def test_idempotency_from_single_duration(duration: Duration) -> None:
    adapter = DurationAdapter(42)

    list(adapter)
    list(adapter)
    durations = list(adapter)

    assert durations == [duration]


@mark.parametrize('sequence', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    (1, 2, 3),
])
def test_construct_from_duration_sequence(sequence: DurationSequence) -> None:
    adapter = DurationAdapter(sequence)

    durations = list(adapter)

    assert durations == [1, 2, 3]


@mark.parametrize('sequence', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    (1, 2, 3),
])
def test_idempotency_from_duration_sequence(sequence: DurationSequence) -> None:
    adapter = DurationAdapter(sequence)

    list(adapter)
    list(adapter)
    durations = list(adapter)

    assert durations == [1, 2, 3]


@mark.parametrize('factory', [
    lambda: [1.0, 2.0, 3.0],
    sequentially(1, 2, 3),
])
def test_construct_from_duration_factory(factory: DurationFactory) -> None:
    adapter = DurationAdapter(factory)

    durations = list(adapter)

    assert durations == [1, 2, 3]


@mark.parametrize('factory', [
    lambda: [1.0, 2.0, 3.0],
    sequentially(1, 2, 3),
])
def test_idempotency_from_duration_factory(factory: DurationFactory) -> None:
    adapter = DurationAdapter(factory)

    list(adapter)
    list(adapter)
    durations = list(adapter)

    assert durations == [1, 2, 3]


@mark.parametrize('durations', [
    -1,
    [-1, 1],
    [1, -1],
])
def test_durations_must_not_be_negative(durations: Durations) -> None:
    with raises(NegativeDurationError, match='Duration must be a positive number or zero'):
        DurationAdapter(durations)


@mark.parametrize('durations', [
    [],
    (),
])
def test_duration_sequence_must_not_be_empty(durations: DurationSequence) -> None:
    with raises(EmptyDurationIterableError, match='Duration iterable must not be empty'):
        DurationAdapter(durations)
