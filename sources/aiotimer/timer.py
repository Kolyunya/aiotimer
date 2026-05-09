from __future__ import annotations

from asyncio import CancelledError, Lock, Task, create_task, sleep
from contextlib import suppress
from time import monotonic_ns
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self, override

from .error import (
    InvalidConfigurationError,
    InvalidDurationError,
    InvalidPrecisionError,
    MissingEventHandlerError,
)
from .event import (
    ErrorEvent,
    IntervalCompleteEvent,
    TimerCompleteEvent,
)
from .state import (
    CompleteState,
    InitialState,
    RunningState,
    State,
    StoppedState,
)
from .timer_interface import TimerInterface
from .utility.callback import Callback, Executor
from .utility.time import ns2s, s2ns

if TYPE_CHECKING:
    from .callback import (
        OnError,
        OnIntervalComplete,
        OnTimerComplete,
    )
    from .interval.type import (
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
        self.__executor: Executor = Executor(
            self.__on_error,
            self.__make_error_event,
        )
        self.__state: State = InitialState()
        self.__interval_generator: IntervalGenerator
        self.__duration: int
        self.__advance_task: Optional[Task[None]] = None
        self.__advanced_at: Optional[int] = None
        self.__elapsed_time: int = 0
        self.__interval_number: int = 0

        self.__initialize_interval_generator()
        if not self.__initialize_next_interval():
            raise InvalidConfigurationError('The interval generator must yield at least one value')

    @override
    async def run(self) -> Self:
        async with self.__lock:
            self.__state.ensure_could_run()
            self.__state = RunningState()

            await self.__start_advancement()

        return self

    @override
    async def pause(self) -> Self:
        async with self.__lock:
            self.__state.ensure_could_stop()
            self.__state = StoppedState()

            await self.__stop_advancement()

        return self

    @override
    async def reset(self) -> Self:
        async with self.__lock:
            self.__state.ensure_could_reset()
            self.__state = InitialState()

            await self.__stop_advancement()
            self.__elapsed_time = 0
            self.__interval_number = 0

            self.__initialize_interval_generator()
            if not self.__initialize_next_interval():
                raise InvalidConfigurationError('The interval generator must yield at least one value')

        return self

    @override
    async def set(self, duration: float) -> Self:
        self.__validate_duration(duration)

        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__duration = s2ns(duration)

        return self

    @override
    async def prolong(self, duration_delta: float) -> Self:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__adjust(duration_delta)

        return self

    @override
    async def shorten(self, duration_delta: float) -> Self:
        async with self.__lock:
            self.__state.ensure_could_adjust()
            self.__adjust(-1 * duration_delta)

        return self

    @override
    async def view(self) -> float:
        async with self.__lock:
            self.__state.ensure_could_view()

            time_left_ns = self.__duration - self.__elapsed_time
            time_left = ns2s(time_left_ns)

            # The timer may (and will) overshoot more or less
            # depending on the duration-to-precision ratio.
            # Return zero in case of an overshoot.
            time_left = max(time_left, 0)

            return time_left

    @override
    async def view_state(self) -> type[State]:
        async with self.__lock:
            return type(self.__state)

    async def __advance(self) -> None:
        try:
            while True:
                async with self.__lock:
                    self.__update_time_counters()

                    if self.__is_interval_complete():
                        await self.__invoke_interval_complete_event()

                        if not self.__initialize_next_interval():
                            self.__state = CompleteState()
                            await self.__invoke_timer_complete_event()
                            return

                await sleep(self.__precision)

        except CancelledError:
            pass

        except Exception as error:
            await self.__invoke_error_event(error)

    def __initialize_interval_generator(self) -> None:
        self.__interval_generator = self.__interval_factory()

    def __initialize_next_interval(self) -> bool:
        success = False

        try:
            duration_seconds = next(self.__interval_generator)
            self.__validate_duration(duration_seconds)
            duration_nseconds = s2ns(duration_seconds)
            self.__duration = duration_nseconds

            self.__advanced_at = None
            self.__elapsed_time = 0
            self.__interval_number += 1

            success = True

        except StopIteration:
            pass

        return success

    async def __start_advancement(self) -> None:
        coroutine = self.__advance()
        self.__advance_task = create_task(coroutine)

    async def __stop_advancement(self) -> None:
        if not self.__advance_task:
            # The advancement task may be missing when
            # `reset()` is called after `stop()`
            return

        self.__advance_task.cancel()
        with suppress(CancelledError):
            await self.__advance_task

        self.__advance_task = None
        self.__advanced_at = None

    def __update_time_counters(self) -> None:
        self.__update_elapsed_time()
        self.__update_advanced_at()

    def __update_elapsed_time(self) -> None:
        if not self.__advanced_at:
            # This is the first iteration of the advancement cycle.
            return

        now = monotonic_ns()
        elapsed = now - self.__advanced_at
        self.__elapsed_time += elapsed

    def __update_advanced_at(self) -> None:
        now = monotonic_ns()
        self.__advanced_at = now

    def __adjust(self, delta: float) -> None:
        delta_ns = s2ns(delta)
        duration = self.__duration + delta_ns

        self.__validate_duration(duration)
        self.__duration = duration

    def __is_interval_complete(self) -> bool:
        is_complete = self.__elapsed_time >= self.__duration

        return is_complete

    def __make_interval_complete_event(self) -> IntervalCompleteEvent:
        event = IntervalCompleteEvent(
            timer=self,
            interval_number=self.__interval_number,
            interval_duration=ns2s(self.__duration),
        )

        return event

    def __make_timer_complete_event(self) -> TimerCompleteEvent:
        event = TimerCompleteEvent(
            timer=self,
            interval_count=self.__interval_number,
        )

        return event

    def __make_error_event(self, error: Exception) -> ErrorEvent:
        event = ErrorEvent(
            timer=self,
            error=error,
        )

        return event

    async def __invoke_interval_complete_event(self) -> None:
        event = self.__make_interval_complete_event()
        await self.__executor(self.__on_interval_complete, event)

    async def __invoke_timer_complete_event(self) -> None:
        event = self.__make_timer_complete_event()
        await self.__executor(self.__on_timer_complete, event)

    async def __invoke_error_event(self, error: Exception) -> None:
        if not self.__on_error.is_set:
            raise error

        event = self.__make_error_event(error)

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
            raise MissingEventHandlerError

    @classmethod
    def __validate_duration(cls, duration: float) -> None:
        if duration < 0:
            raise InvalidDurationError

    @classmethod
    def __validate_precision(cls, precision: float) -> None:
        if precision <= 0:
            raise InvalidPrecisionError
