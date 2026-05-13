from asyncio import sleep
from unittest.mock import Mock

from pytest import mark

from aiotimer import Timer
from aiotimer.interval import once
from aiotimer.state import CompleteState, InitialState, RunningState, StoppedState


@mark.asyncio
async def test_initial_state_after_instantiating() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    state = await timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_running_state() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    await timer.run()
    state = await timer.state

    # Assert
    assert state == RunningState


@mark.asyncio
async def test_stopped_state_after_stopping() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    await timer.run()
    await timer.pause()
    state = await timer.state

    # Assert
    assert state == StoppedState


@mark.asyncio
async def test_complete_state() -> None:
    # Arrange
    timer = Timer(once(0.1), Mock())

    # Act
    await timer.run()
    await sleep(1)
    state = await timer.state

    # Assert
    assert state == CompleteState


@mark.asyncio
async def test_initial_state_after_running_and_resetting() -> None:
    # Arrange
    timer = Timer(once(1), Mock())

    # Act
    await timer.run()
    await timer.reset()
    state = await timer.state

    # Assert
    assert state == InitialState


@mark.asyncio
async def test_initial_state_after_completing_and_resetting() -> None:
    # Arrange
    timer = Timer(once(0.1), Mock())

    # Act
    await timer.run()
    await sleep(1)
    await timer.reset()
    state = await timer.state

    # Assert
    assert state == InitialState
