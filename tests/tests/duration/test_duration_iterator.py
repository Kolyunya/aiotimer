from typing import Union

from pytest import mark, raises

from aiotimer.duration import DurationIterator
from aiotimer.error import InvalidDurationError


def test_invalid_durations() -> None:
    class InvalidDuration:
        pass

    with raises(InvalidDurationError) as error:
        DurationIterator(InvalidDuration())  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

    assert str(error.value) == 'Invalid duration provided'


@mark.parametrize('duration', [42.0, 42])
def test_durations_from_a_single_number(duration: Union[float, int]) -> None:
    iterator = DurationIterator(42)

    durations = list(iter(iterator))

    assert durations == [duration]


@mark.parametrize('duration', [42.0, 42])
def test_idempotency_for_a_single_number(duration: Union[float, int]) -> None:
    iterator = DurationIterator(42)

    durations = list(iter(iterator))
    durations = list(iter(iterator))

    assert durations == [duration]


@mark.parametrize('durations_list', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
])
def test_durations_from_a_list_of_numbers(durations_list: list[float]) -> None:
    iterator = DurationIterator(durations_list)

    durations = list(iter(iterator))

    assert durations == [1, 2, 3]


@mark.parametrize('durations_list', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
])
def test_idempotency_for_a_list_of_numbers(durations_list: list[float]) -> None:
    iterator = DurationIterator(durations_list)

    durations = list(iter(iterator))
    durations = list(iter(iterator))

    assert durations == [1, 2, 3]


@mark.parametrize('durations_list', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
])
def test_durations_from_an_iterable_factory(durations_list: list[float]) -> None:
    factory = lambda: durations_list
    iterator = DurationIterator(factory)

    durations = list(iter(iterator))

    assert durations == [1, 2, 3]


@mark.parametrize('durations_list', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
])
def test_idempotency_for_an_iterable_factory(durations_list: list[float]) -> None:
    factory = lambda: durations_list
    iterator = DurationIterator(factory)

    durations = list(iter(iterator))
    durations = list(iter(iterator))

    assert durations == [1, 2, 3]
