from asyncio import sleep
from unittest.mock import Mock

from pytest import mark, raises

from aiotimer import Timer
from aiotimer.error import InvalidStateError
from aiotimer.interval import once


@mark.asyncio
async def test_could_not_run_while_running() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    await timer.run()

    with raises(InvalidStateError) as error:
        await timer.run()

    # Assert
    assert str(error.value) == 'The timer could not be run while in the running state'


@mark.asyncio
async def test_could_not_run_after_completion() -> None:
    # Arrange
    timer = Timer(once(0.1), Mock())

    # Act
    await timer.run()
    await sleep(1)

    with raises(InvalidStateError) as error:
        await timer.run()

    # Assert
    assert str(error.value) == 'The timer could not be run while in the complete state'


@mark.asyncio
async def test_can_not_stop_while_in_the_initial_state() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(InvalidStateError) as error:
        await timer.pause()

    assert str(error.value) == 'The timer could not be stopped while in the initial state'


@mark.asyncio
async def test_could_not_stop_after_completion() -> None:
    # Arrange
    timer = Timer(once(0.1), Mock())

    # Act
    await timer.run()
    await sleep(1)

    with raises(InvalidStateError) as error:
        await timer.pause()

    # Assert
    assert str(error.value) == 'The timer could not be stopped while in the complete state'


@mark.asyncio
async def test_can_not_reset_while_in_initial_state() -> None:
    # Arrange
    timer = Timer(once(42), Mock())

    # Act
    with raises(InvalidStateError) as error:
        await timer.reset()

    assert str(error.value) == 'The timer could not be reset while in the initial state'
