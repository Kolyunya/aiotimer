from __future__ import annotations

from asyncio import CancelledError, Lock, Queue, Task, create_task, sleep
from contextlib import suppress
from time import monotonic
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from .callback import (
    AsyncExecutor,
    Callback,
    Executor,
    SyncExecutor,
)
from .error import (
    EmptyGeneratorError,
    InvalidPrecisionError,
    MissingEventHandlerError,
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
    from collections.abc import Awaitable

    from .callback import (
        OnError,
        OnIntervalComplete,
        OnTimerComplete,
    )
    from .interval import (
        IntervalGenerator,
        IntervalGeneratorFactory,
    )


class Timer(TimerInterface):

    def __init__(
        self,
        interval_factory: IntervalGeneratorFactory,
        on_timer_complete: Optional[OnTimerComplete] = None,
        on_interval_complete: Optional[OnIntervalComplete] = None,
        on_error: Optional[OnError] = None,
        *,
        await_callbacks: bool = False,
        precision: float = 0.1,
    ) -> None:
        self.__validate_event_handlers(on_timer_complete, on_interval_complete)
        self.__validate_precision(precision)

        self.__interval_factory = interval_factory
        self.__on_timer_complete = Callback(on_timer_complete)
        self.__on_interval_complete = Callback(on_interval_complete)
        self.__on_error = Callback(on_error)
        self.__precision = precision

        self.__lock: Lock = Lock()
        self.__state: State = InitialState()
        self.__advancement_task: Optional[Task[None]] = None
        self.__callbacks: Queue[Awaitable[None]] = Queue()
        self.__started_at: Optional[float] = None

        self.__executor: Executor
        self.__initialize_executor(await_callbacks=await_callbacks)

        self.__interval_generator: IntervalGenerator
        self.__initialize_interval_generator()

        self.__interval: Interval
        if not self.__initialize_next_interval(first_one=True):
            raise EmptyGeneratorError

    @override
    async def run(self) -> None:
        async with self.__lock:
            self.__state.ensure_could_run()
            self.__state = RunningState()
            self.__started_at = monotonic()

            await self.__start_advancement()

    @override
    async def pause(self) -> None:
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

            self.__started_at = None

            self.__initialize_interval_generator()
            if not self.__initialize_next_interval(first_one=True):
                raise EmptyGeneratorError

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
    async def remaining_time(self) -> float:
        async with self.__lock:
            self.__state.ensure_could_view()
            remaining_time = self.__interval.remaining_time

            return remaining_time

    @property
    @override
    async def elapsed_time(self) -> float:
        async with self.__lock:
            elapsed_time = self.__get_elapsed_time()

            return elapsed_time

    @property
    @override
    async def state(self) -> type[State]:
        async with self.__lock:
            return type(self.__state)

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

                            # Stop the advancement.
                            break

                await self.__process_callbacks()

                await sleep(self.__precision)

        except CancelledError:
            pass

        except Exception as error:
            await self.__invoke_error_event(error)

        finally:
            await self.__process_callbacks()

    def __initialize_executor(self, *, await_callbacks: bool) -> None:
        executor_type = SyncExecutor if await_callbacks else AsyncExecutor
        self.__executor = executor_type(
            self.__on_error,
            self.__make_error_event,
        )

    def __initialize_interval_generator(self) -> None:
        self.__interval_generator = self.__interval_factory()

    def __initialize_next_interval(self, *, first_one: bool = False) -> bool:
        success = False

        try:
            duration = next(self.__interval_generator)

            if first_one:
                number = 1
            else:
                number = self.__interval.number + 1

            self.__interval = Interval(number, duration)
            success = True

        except StopIteration:
            pass

        return success

    async def __start_advancement(self) -> None:
        coroutine = self.__advance()
        self.__advancement_task = create_task(coroutine)

    async def __stop_advancement(self) -> None:
        if not self.__advancement_task:
            # The advancement task may be missing when
            # `reset()` is called after `stop()`
            return

        self.__advancement_task.cancel()
        with suppress(CancelledError):
            await self.__advancement_task

        self.__advancement_task = None
        self.__interval.stop_advancement()

    async def __process_callbacks(self) -> None:
        while not self.__callbacks.empty():
            callback = await self.__callbacks.get()
            await callback
            self.__callbacks.task_done()

    async def __make_interval_complete_event(self) -> IntervalCompleteEvent:
        elapsed = self.__get_elapsed_time()
        event = IntervalCompleteEvent(
            timer=self,
            elapsed=elapsed,
            interval_number=self.__interval.number,
            interval_duration=self.__interval.duration,
        )

        return event

    async def __make_timer_complete_event(self) -> TimerCompleteEvent:
        elapsed = self.__get_elapsed_time()
        event = TimerCompleteEvent(
            timer=self,
            elapsed=elapsed,
            interval_count=self.__interval.number,
        )

        return event

    async def __make_error_event(self, error: Exception) -> ErrorEvent:
        elapsed = self.__get_elapsed_time()
        event = ErrorEvent(
            timer=self,
            elapsed=elapsed,
            error=error,
        )

        return event

    async def __enqueue_interval_complete_event(self) -> None:
        event = await self.__make_interval_complete_event()
        coroutine = self.__executor(self.__on_interval_complete, event)
        await self.__callbacks.put(coroutine)

    async def __enqueue_timer_complete_event(self) -> None:
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

    def __get_elapsed_time(self) -> float:
        elapsed_time = 0.0

        if self.__started_at is not None:
            now = monotonic()
            elapsed_time = now - self.__started_at

        return elapsed_time

    @classmethod
    def __validate_event_handlers(
            cls,
            on_complete: Optional[OnTimerComplete],
            on_interval: Optional[OnIntervalComplete],
    ) -> None:
        if not on_complete and not on_interval:
            raise MissingEventHandlerError

    @classmethod
    def __validate_precision(cls, precision: float) -> None:
        if precision <= 0:
            raise InvalidPrecisionError
