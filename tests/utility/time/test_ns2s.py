from pytest import mark

from aiotimer.utility.time import s2ns


@mark.parametrize(('seconds', 'nano_seconds_expected'), [
    (0.0, 0),
    (1.0, 1_000_000_000),
    (42.123_456_789, 42_123_456_789),
])
def test_s2ns(seconds: float, nano_seconds_expected: int) -> None:
    nano_seconds = s2ns(seconds)

    assert nano_seconds_expected == nano_seconds


def test_s2ns_rounds_to_closes_integer() -> None:
    seconds = 0.000_000_000_9

    nano_seconds = s2ns(seconds)

    assert nano_seconds == 1
