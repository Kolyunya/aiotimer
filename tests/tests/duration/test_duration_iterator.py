from typing import Union

from pytest import mark

from aiotimer.duration import DurationIterator


@mark.parametrize('duration', [42.0, 42])
def test_durations_from_a_single_number(duration: Union[float, int]) -> None:
    iterator = DurationIterator(42)

    durations = list(iter(iterator))

    assert durations == [duration]


@mark.parametrize('duration', [42.0, 42])
def test_idempotency_for_a_single_number(duration: Union[float, int]) -> None:
    iterator = DurationIterator(42)

    list(iter(iterator))
    list(iter(iterator))
    durations = list(iter(iterator))

    assert durations == [duration]


@mark.parametrize('durations_collection', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    (1, 2, 3),
])
def test_durations_from_a_collection_of_numbers(
    durations_collection: Union[list[float], tuple[float, ...]],
) -> None:
    iterator = DurationIterator(durations_collection)

    durations = list(iter(iterator))

    assert durations == [1, 2, 3]


@mark.parametrize('durations_collection', [
    [1.0, 2.0, 3.0],
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    (1, 2, 3),
])
def test_idempotency_for_a_collection_of_numbers(
        durations_collection: Union[list[float], tuple[float, ...]],
) -> None:
    iterator = DurationIterator(durations_collection)

    list(iter(iterator))
    list(iter(iterator))
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

    list(iter(iterator))
    list(iter(iterator))
    durations = list(iter(iterator))

    assert durations == [1, 2, 3]
