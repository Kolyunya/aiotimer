from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import MultiTimer
from aiotimer.duration import once
from aiotimer.error import InvalidStateError


@mark.asyncio
async def test_could_not_run_while_running() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    await timer.start()

    with raises(InvalidStateError) as error:
        await timer.start()

    # Assert
    assert str(error.value) == 'The timer could not be started while in the running state'


@mark.asyncio
async def test_could_not_run_after_completion() -> None:
    # Arrange
    timer = MultiTimer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)

    with raises(InvalidStateError) as error:
        await timer.start()

    # Assert
    assert str(error.value) == 'The timer could not be started while in the complete state'


@mark.asyncio
async def test_can_not_stop_while_in_the_initial_state() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    with raises(InvalidStateError) as error:
        await timer.stop()

    assert str(error.value) == 'The timer could not be stopped while in the initial state'


@mark.asyncio
async def test_could_not_stop_after_completion() -> None:
    # Arrange
    timer = MultiTimer(once(0.1), Mock())

    # Act
    await timer.start()
    await sleep(1)

    with raises(InvalidStateError) as error:
        await timer.stop()

    # Assert
    assert str(error.value) == 'The timer could not be stopped while in the complete state'


@mark.asyncio
async def test_can_not_reset_while_in_initial_state() -> None:
    # Arrange
    timer = MultiTimer(once(42), Mock())

    # Act
    with raises(InvalidStateError) as error:
        await timer.reset()

    assert str(error.value) == 'The timer could not be reset while in the initial state'
