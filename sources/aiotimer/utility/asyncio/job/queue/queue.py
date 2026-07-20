from asyncio import Queue, create_task, shield
from collections.abc import Awaitable
from typing import Any

from typing_extensions import override

from .queue_interface import JobQueueInterface


class JobQueue(JobQueueInterface):

    def __init__(self) -> None:
        self.__jobs = Queue[Awaitable[Any]]()

    @override
    async def push(self, job: Awaitable[Any]) -> None:
        await self.__jobs.put(job)

    @override
    async def process(self) -> None:
        # Job processing must be offloaded to a separate task
        # in order to support the parent coroutine cancellation.
        # The task must also be shielded for the same very reason.

        if self.__jobs.empty():
            return

        async def process_jobs() -> None:
            while not self.__jobs.empty():
                job = await self.__jobs.get()
                await job
                self.__jobs.task_done()

        await shield(create_task(process_jobs()))
