from __future__ import annotations

from asyncio import (
    CancelledError,
    Event,
    Lock,
    Queue,
    Task,
    create_task,
    sleep,
)
from collections.abc import Awaitable, Iterator
from contextlib import suppress
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from .callback import (
    AsyncExecutor,
    Callback,
    Executor,
    SyncExecutor,
)
from .error import (
    EmptyDurationIterableError,
    InvalidPrecisionError,
    MissingCallbackError,
)
from .event import (
    ErrorEvent,
    IntervalCompleteEvent,
    TimerCompleteEvent,
)
from .interval import Interval
from .state import (
    CompleteState,
    InitialState,
    RunningState,
    State,
    StoppedState,
)
from .timer_interface import TimerInterface

if TYPE_CHECKING:
    from .callback import (
        OnError,
        OnIntervalComplete,
        OnTimerComplete,
    )
    from .duration import DurationFactory


class Timer(TimerInterface):

    def __init__(
        self,
        duration_factory: DurationFactory,
        on_timer_complete: Optional[OnTimerComplete] = None,
        on_interval_complete: Optional[OnIntervalComplete] = None,
        on_error: Optional[OnError] = None,
        *,
        precision: float = 0.001,
        await_callbacks: bool = False,
    ) -> None:
        self.__validate_event_handlers(on_timer_complete, on_interval_complete)
        self.__validate_precision(precision)

        self.__duration_factory = duration_factory
        self.__on_timer_complete = Callback(on_timer_complete)
        self.__on_interval_complete = Callback(on_interval_complete)
        self.__on_error = Callback(on_error)
        self.__precision = precision

        self.__lock: Lock = Lock()
        self.__modified: Event = Event()

        self.__state: State = InitialState()
        self.__advance_task: Optional[Task[None]] = None
        self.__callbacks: Queue[Awaitable[None]] = Queue[Awaitable[None]]()

        self.__executor: Executor
        self.__initialize_executor(await_callbacks=await_callbacks)

        self.__duration_iterator: Iterator[float]
        self.__initialize_duration_iterator()

        self.__interval: Interval
        if not self.__initialize_next_interval(reset=True):
            raise EmptyDurationIterableError

    @override
    async def start(self) -> None:
        async with self.__lock:
            self.__state.ensure_could_start()
            self.__state = RunningState()
            await self.__start_advancement()

    @override
    async def stop(self) -> None:
        async with self.__lock:
            self.__state.ensure_could_stop()
            self.__state = StoppedState()
            await self.__stop_advancement()

    @override
    async def reset(self) -> None:
        async with self.__lock:
            self.__state.ensure_could_reset()
            self.__state = InitialState()
            await self.__stop_advancement()

            self.__initialize_duration_iterator()
            if not self.__initialize_next_interval(reset=True):
                raise EmptyDurationIterableError

    @override
    async def set(self, duration: float) -> None:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__interval.duration = duration
            self.__modified.set()

    @override
    async def prolong(self, delta: float) -> None:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__interval.prolong(delta)
            self.__modified.set()

    @override
    async def shorten(self, delta: float) -> None:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__interval.shorten(delta)
            self.__modified.set()

    @property
    @override
    async def remaining(self) -> float:
        async with self.__lock:
            return self.__interval.remaining

    @property
    @override
    async def elapsed(self) -> float:
        async with self.__lock:
            return self.__interval.elapsed

    @property
    @override
    async def state(self) -> type[State]:
        async with self.__lock:
            return type(self.__state)

    async def __start_advancement(self) -> None:
        self.__interval.start()

        self.__advance_task = create_task(self.__advance())

    async def __stop_advancement(self) -> None:
        if not self.__advance_task:
            # The run task will be missing when
            # `reset()` is called after `stop()`.
            return

        self.__interval.stop()

        self.__advance_task.cancel()
        with suppress(CancelledError):
            await self.__advance_task
        self.__advance_task = None

    async def __advance(self) -> None:
        try:
            while True:
                async with self.__lock:
                    self.__interval.advance()

                    if self.__interval.is_complete:
                        await self.__enqueue_interval_complete_event()

                        if not self.__initialize_next_interval():
                            self.__state = CompleteState()
                            await self.__enqueue_timer_complete_event()
                            break

                # The lock must be released before callback processing.
                await self.__process_callbacks()

                await sleep(self.__precision)

        except Exception as error:
            await self.__invoke_error_event(error)

        finally:
            await self.__process_callbacks()

    async def __process_callbacks(self) -> None:
        while not self.__callbacks.empty():
            callback = await self.__callbacks.get()
            await callback
            self.__callbacks.task_done()

    def __initialize_executor(self, *, await_callbacks: bool) -> None:
        executor_type = SyncExecutor if await_callbacks else AsyncExecutor
        self.__executor = executor_type(
            self.__on_error,
            self.__make_error_event,
        )

    def __initialize_duration_iterator(self) -> None:
        iterable = self.__duration_factory()
        iterator = iter(iterable)

        self.__duration_iterator = iterator

    def __initialize_next_interval(self, *, reset: bool = False) -> bool:
        success = False

        try:
            duration = next(self.__duration_iterator)

            if reset:
                number = 1
            else:
                number = self.__interval.number + 1

            self.__interval = Interval(number, duration)
            if isinstance(self.__state, RunningState):
                self.__interval.start()

            success = True

        except StopIteration:
            pass

        return success

    async def __make_interval_complete_event(self) -> IntervalCompleteEvent:
        event = IntervalCompleteEvent(
            timer=self,
            elapsed=self.__interval.elapsed,
            remaining=self.__interval.remaining,
            interval_number=self.__interval.number,
            interval_duration=self.__interval.duration,
        )

        return event

    async def __make_timer_complete_event(self) -> TimerCompleteEvent:
        event = TimerCompleteEvent(
            timer=self,
            elapsed=self.__interval.elapsed,
            remaining=self.__interval.remaining,
            interval_count=self.__interval.number,
        )

        return event

    async def __make_error_event(self, error: Exception) -> ErrorEvent:
        event = ErrorEvent(
            timer=self,
            elapsed=self.__interval.elapsed,
            remaining=self.__interval.remaining,
            error=error,
        )

        return event

    async def __enqueue_interval_complete_event(self) -> None:
        if self.__on_interval_complete.is_missing:
            return

        event = await self.__make_interval_complete_event()
        coroutine = self.__executor(self.__on_interval_complete, event)
        await self.__callbacks.put(coroutine)

    async def __enqueue_timer_complete_event(self) -> None:
        if self.__on_timer_complete.is_missing:
            return

        event = await self.__make_timer_complete_event()
        coroutine = self.__executor(self.__on_timer_complete, event)
        await self.__callbacks.put(coroutine)

    async def __invoke_error_event(self, error: Exception) -> None:
        event = await self.__make_error_event(error)

        await self.__executor(
            self.__on_error,
            event,

            # Disable error handling to prevent an infinite loop
            # in case an error occurs inside the error handler.
            handle_errors=False,
        )

    @classmethod
    def __validate_event_handlers(
            cls,
            on_complete: Optional[OnTimerComplete],
            on_interval: Optional[OnIntervalComplete],
    ) -> None:
        if not on_complete and not on_interval:
            raise MissingCallbackError

    @classmethod
    def __validate_precision(cls, precision: float) -> None:
        if precision <= 0:
            raise InvalidPrecisionError
