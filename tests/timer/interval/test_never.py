from aiotimer.interval.never import never


def test_never() -> None:
    # Arrange
    factory = never()
    generator = factory()

    # Act
    durations = list(generator)

    # Assert
    assert len(durations) == 0
