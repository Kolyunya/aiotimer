# `wait_for()` raises `asyncio.TimeoutError`, which is a distinct class from the
# builtin `TimeoutError` until Python 3.11. Drop the corresponding import and
# catch the builtin `TimeoutError` directly once support for Python 3.10 is dropped.
from asyncio import Event, create_task, sleep, wait_for
from asyncio import TimeoutError as AsyncTimeoutError
from contextlib import suppress
from unittest.mock import AsyncMock

from pytest import mark, raises

from aiotimer.utility.asyncio.job.queue import JobQueue


@mark.asyncio
async def test_can_process_empty_queue() -> None:
    # Arrange
    queue = JobQueue()

    # Act
    await queue.process()

    # Assert
    # No exceptions thrown.


@mark.asyncio
async def test_can_push_and_process_job() -> None:
    # Arrange
    queue = JobQueue()
    job = AsyncMock()

    # Act
    await queue.push(job())
    await queue.process()

    # Assert
    assert job.await_count == 1


@mark.asyncio
async def test_jobs_are_processed_in_fifo_order() -> None:
    # Arrange
    queue = JobQueue()
    jobs: list[int] = []

    async def job(number: int) -> None:
        jobs.append(number)

    # Act
    await queue.push(job(1))
    await queue.push(job(2))
    await queue.push(job(3))
    await queue.process()

    # Assert
    assert jobs == [1, 2, 3]


@mark.asyncio
async def test_job_exception_propagates_to_process_caller() -> None:
    # Arrange
    queue = JobQueue()

    error = RuntimeError('Job error')
    job = AsyncMock(side_effect=error)

    await queue.push(job())

    # Act / Assert
    with raises(RuntimeError, match='Job error'):
        await queue.process()


@mark.asyncio
async def test_processing_survives_parent_cancellation() -> None:
    # Arrange
    queue = JobQueue()
    started = Event()
    complete = Event()

    async def trigger(event: Event) -> None:
        event.set()

    # Act
    await queue.push(trigger(started))
    await queue.push(sleep(1))
    await queue.push(trigger(complete))

    process = create_task(queue.process())
    await started.wait()
    process.cancel()

    with suppress(AsyncTimeoutError):
        await wait_for(complete.wait(), 2)

    # Assert
    assert process.cancelled()
    assert complete.is_set()
