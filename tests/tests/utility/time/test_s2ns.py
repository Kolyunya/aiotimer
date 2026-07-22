from pytest import mark

from aiotimer.utility.time import s2ns


@mark.parametrize(('seconds', 'nano_seconds_expected'), [
    (0.0, 0),
    (1.0, 1_000_000_000),
    (42.123_456_789, 42_123_456_789),
])
def test_s2ns(seconds: float, nano_seconds_expected: int) -> None:
    nano_seconds = s2ns(seconds)

    assert nano_seconds == nano_seconds_expected


@mark.parametrize(('seconds', 'nano_seconds_expected'), [
    (0.000_000_000_100, 0),
    (0.000_000_000_400, 0),
    (0.000_000_000_501, 1),
    (0.000_000_000_900, 1),
])
def test_s2ns_rounds_to_closest_integer(seconds: float, nano_seconds_expected: int) -> None:
    nano_seconds = s2ns(seconds)

    assert nano_seconds == nano_seconds_expected
