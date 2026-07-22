from aiotimer.duration.factory import never


def test_never() -> None:
    # Arrange
    factory = never()

    # Act
    durations = list(factory())

    # Assert
    assert len(durations) == 0
