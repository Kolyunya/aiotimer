from aiotimer.duration.multiplier import (
    day,
    days,
    hour,
    hours,
    millisecond,
    milliseconds,
    minute,
    minutes,
    month,
    months,
    second,
    seconds,
    week,
    weeks,
    year,
    years,
)


def test_millisecond() -> None:
    assert millisecond == 0.001
    assert milliseconds == millisecond


def test_second() -> None:
    assert second == 1
    assert seconds == second


def test_minute() -> None:
    assert minute == 60
    assert minutes == minute


def test_hour() -> None:
    assert hour == 60 * 60
    assert hours == hour


def test_day() -> None:
    assert day == 24 * 60 * 60
    assert days == day


def test_week() -> None:
    assert week == 7 * 24 * 60 * 60
    assert weeks == week


def test_month() -> None:
    assert month == 30 * 24 * 60 * 60
    assert months == month


def test_year() -> None:
    assert year == 365 * 24 * 60 * 60
    assert years == year
