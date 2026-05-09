from pytest import mark

from aiotimer.utility.time import ns2s


@mark.parametrize(('nanoseconds', 'seconds_expected'), [
    (0, 0.0),
    (1_000_000_000, 1.0),
    (42_123_456_789, 42.123_456_789),
])
def test_s2ns(nanoseconds: int, seconds_expected: float) -> None:
    seconds = ns2s(nanoseconds)

    assert seconds_expected == seconds
