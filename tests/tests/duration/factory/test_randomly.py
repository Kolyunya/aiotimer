from pytest import approx, mark, raises

from aiotimer.duration.factory import randomly
from aiotimer.error import InvalidDurationError


@mark.parametrize(('minimum', 'maximum'), [
    (2, 1),
    (2, 2),
])
def test_minimum_duration_must_be_less_than_maximum_duration(
        minimum: float,
        maximum: float,
) -> None:
    with raises(InvalidDurationError) as error:
        randomly(minimum, maximum)

    assert str(error.value) == 'Minimum duration must be less than maximum duration'


@mark.parametrize(('minimum', 'maximum'), [
    (-1, 1),
    (0, 1),
])
def test_duration_boundaries_must_be_positive(
    minimum: float,
    maximum: float,
) -> None:
    with raises(InvalidDurationError) as error:
        randomly(minimum, maximum)

    assert str(error.value) == 'Duration boundaries must be positive numbers'


def test_randomly() -> None:
    # Arrange
    factory = randomly(3, 5)

    # Act
    for _ in range(100):
        durations = list(factory())

        assert len(durations) == 1
        assert durations[0] == approx(4, abs=1)
