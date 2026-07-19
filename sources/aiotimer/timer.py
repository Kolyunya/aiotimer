from __future__ import annotations

from asyncio import (
    CancelledError,
    Lock,
    Queue,
    Task,
    create_task,
    shield,
    sleep,
)
from collections.abc import Awaitable, Iterator
from contextlib import suppress
from typing import Optional

from typing_extensions import override

from .callback import (
    AsyncExecutor,
    Callback,
    ExecutorInterface,
    OnError,
    OnIntervalComplete,
    OnTimerComplete,
    SyncExecutor,
)
from .duration import DurationFactory
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
    FailedState,
    InitialState,
    RunningState,
    StateInterface,
    StoppedState,
)
from .timer_interface import TimerInterface


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
        self.__state: StateInterface = InitialState()
        self.__advance_task: Optional[Task[None]] = None
        self.__callbacks: Queue[Awaitable[None]] = Queue[Awaitable[None]]()

        self.__executor: ExecutorInterface
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

    @override
    async def prolong(self, delta: float) -> None:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__interval.prolong(delta)

    @override
    async def shorten(self, delta: float) -> None:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__interval.shorten(delta)

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
    async def state(self) -> type[StateInterface]:
        async with self.__lock:
            return type(self.__state)

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

            success = True

        except StopIteration:
            pass

        return success

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
                await self.__process_events()

                await sleep(self.__precision)

        except Exception as error:
            await self.__enqueue_error_event(error)
            self.__state = FailedState()

        finally:
            await self.__process_events()

    async def __enqueue_interval_complete_event(self) -> None:
        if self.__on_interval_complete.is_missing:
            return

        event = await self.__make_interval_complete_event()
        coroutine = self.__executor.execute(self.__on_interval_complete, event)
        await self.__callbacks.put(coroutine)

    async def __enqueue_timer_complete_event(self) -> None:
        if self.__on_timer_complete.is_missing:
            return

        event = await self.__make_timer_complete_event()
        coroutine = self.__executor.execute(self.__on_timer_complete, event)
        await self.__callbacks.put(coroutine)

    async def __enqueue_error_event(self, error: Exception) -> None:
        coroutine = self.__executor.handle_error(error)
        await self.__callbacks.put(coroutine)

    async def __make_interval_complete_event(self) -> IntervalCompleteEvent:
        event = IntervalCompleteEvent(
            timer=self,
            interval_number=self.__interval.number,
            interval_duration=self.__interval.duration,
        )

        return event

    async def __make_timer_complete_event(self) -> TimerCompleteEvent:
        event = TimerCompleteEvent(
            timer=self,
            interval_count=self.__interval.number,
        )

        return event

    async def __make_error_event(self, error: Exception) -> ErrorEvent:
        event = ErrorEvent(
            timer=self,
            error=error,
        )

        return event

    async def __process_events(self) -> None:
        # Event processing must be offloaded to a separate task in order to
        # support stopping and resetting from the inside of event handlers.
        # The task must also be shielded to protect it from the cancel-propagation
        # from the `__advance()` task when it is canceled during stopping and resetting.

        async def process_events() -> None:
            while not self.__callbacks.empty():
                callback = await self.__callbacks.get()
                await callback
                self.__callbacks.task_done()

        if not self.__callbacks.empty():
            await shield(create_task(process_events()))

    @classmethod
    def __validate_event_handlers(
            cls,
            on_timer_complete: Optional[OnTimerComplete],
            on_interval_complete: Optional[OnIntervalComplete],
    ) -> None:
        if on_timer_complete is None and on_interval_complete is None:
            raise MissingCallbackError

    @classmethod
    def __validate_precision(cls, precision: float) -> None:
        if precision <= 0:
            raise InvalidPrecisionError
