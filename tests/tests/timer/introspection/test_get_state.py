from asyncio import sleep
from unittest.mock import Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.duration import once
from aiotimer.state import CompleteState, InitialState, RunningState, StoppedState


@mark.asyncio
async def test_see_initial_state_after_instantiation() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    state = timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_see_running_state_after_starting() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    await timer.start()

    state = timer.state

    # Assert
    assert state == RunningState


@mark.asyncio
async def test_see_stopped_state_after_stopping() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    await timer.start()
    await timer.stop()

    state = timer.state

    # Assert
    assert state == StoppedState


@mark.asyncio
async def test_complete_state_after_completion() -> None:
    # Arrange
    timer = Timer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)

    state = timer.state

    # Assert
    assert state == CompleteState


@mark.asyncio
async def test_see_initial_state_after_starting_and_resetting() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    await timer.start()
    await timer.reset()

    state = timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_see_initial_state_after_completion_and_resetting() -> None:
    # Arrange
    timer = Timer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)
    await timer.reset()

    state = timer.state

    # Assert
    assert state == InitialState
