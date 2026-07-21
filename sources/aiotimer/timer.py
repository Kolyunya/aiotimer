from __future__ import annotations

from asyncio import (
    CancelledError,
    Lock,
    Task,
    create_task,
    sleep,
)
from collections.abc import Coroutine, Iterator
from contextlib import suppress
from typing import Any, Optional

from typing_extensions import override

from .callback import (
    Callback,
    OnError,
    OnIntervalComplete,
    OnTimerComplete,
)
from .duration import DurationAdapter, Durations
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
from .utility.asyncio.coroutine.executor import (
    AsyncExecutor,
    ExecutorInterface,
    SyncExecutor,
)
from .utility.asyncio.error.handler import (
    ErrorHandler,
    ErrorHandlerInterface,
)
from .utility.asyncio.job.queue import JobQueue


class Timer(TimerInterface):

    def __init__(
        self,
        durations: Durations,
        on_timer_complete: Optional[OnTimerComplete] = None,
        on_interval_complete: Optional[OnIntervalComplete] = None,
        on_error: Optional[OnError] = None,
        *,
        precision: float = 0.001,
        await_callbacks: bool = False,
    ) -> None:
        self.__validate_event_handlers(on_timer_complete, on_interval_complete)
        self.__validate_precision(precision)

        self.__duration_adapter = DurationAdapter(durations)
        self.__on_timer_complete = Callback(on_timer_complete)
        self.__on_interval_complete = Callback(on_interval_complete)
        self.__on_error = Callback(on_error)
        self.__precision = precision

        self.__lock: Lock = Lock()
        self.__state: StateInterface = InitialState()
        self.__advance_task: Optional[Task[None]] = None
        self.__callbacks = JobQueue()

        self.__error_handler: ErrorHandlerInterface
        self.__initialize_error_handler()

        self.__executor: ExecutorInterface
        self.__initialize_executor(await_callbacks=await_callbacks)

        self.__duration_iterator: Iterator[float]
        self.__initialize_duration_iterator()

        self.__interval: Interval
        self.__initialize_next_interval(reset=True)

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
            self.__initialize_next_interval(reset=True)

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
    def remaining(self) -> float:
        return self.__interval.remaining

    @property
    @override
    def elapsed(self) -> float:
        return self.__interval.elapsed

    @property
    @override
    def state(self) -> type[StateInterface]:
        return type(self.__state)

    def __initialize_error_handler(self) -> None:
        if self.__on_error.is_missing:
            self.__error_handler = ErrorHandler(None)

        else:
            async def handle_error(error: Exception) -> None:
                event = await self.__make_error_event(error)
                await self.__on_error(event)

            self.__error_handler = ErrorHandler(handle_error)

    def __initialize_executor(self, *, await_callbacks: bool) -> None:
        executor_type = SyncExecutor if await_callbacks else AsyncExecutor
        self.__executor = executor_type(self.__error_handler)

    def __initialize_duration_iterator(self) -> None:
        self.__duration_iterator = iter(self.__duration_adapter)

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

        if reset and not success:
            raise EmptyDurationIterableError

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
                        await self.__enqueue_interval_complete_callback()

                        if not self.__initialize_next_interval():
                            self.__state = CompleteState()
                            await self.__enqueue_timer_complete_callback()
                            break

                # The lock must be released before callback processing.
                await self.__callbacks.process()

                await sleep(self.__precision)

        except Exception as error:
            await self.__enqueue_error_callback(error)
            self.__state = FailedState()

        finally:
            await self.__callbacks.process()

    async def __enqueue_interval_complete_callback(self) -> None:
        if self.__on_interval_complete.is_missing:
            return

        event = await self.__make_interval_complete_event()
        callback = self.__on_interval_complete(event)
        await self.__enqueue_callback(callback)

    async def __enqueue_timer_complete_callback(self) -> None:
        if self.__on_timer_complete.is_missing:
            return

        event = await self.__make_timer_complete_event()
        callback = self.__on_timer_complete(event)
        await self.__enqueue_callback(callback)

    async def __enqueue_error_callback(self, error: Exception) -> None:
        callback = self.__error_handler.handle(error)

        # Enable error-bubbling to the event loop.
        # Failing to do so results in an infinite loop inside a failing error handler.
        await self.__enqueue_callback(callback, bubble_errors=True)

    async def __enqueue_callback(self, callback: Coroutine[Any, Any, None], *, bubble_errors: bool = False) -> None:
        callback = self.__executor.execute(callback, bubble_errors=bubble_errors)
        await self.__callbacks.push(callback)

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
