from __future__ import annotations

from asyncio import CancelledError, Lock, Task, create_task, sleep
from contextlib import suppress
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from .callback import Callback, Executor
from .error import (
    InvalidConfigurationError,
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
        self.__advancement_task: Optional[Task[None]] = None
        self.__interval_generator: IntervalGenerator
        self.__interval: Interval

        self.__initialize_interval_generator()
        if not self.__initialize_next_interval(first_one=True):
            raise InvalidConfigurationError('The interval generator must yield at least one value')

    @override
    async def run(self) -> None:
        async with self.__lock:
            self.__state.ensure_could_run()
            self.__state = RunningState()

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

            self.__initialize_interval_generator()
            if not self.__initialize_next_interval(first_one=True):
                raise InvalidConfigurationError('The interval generator must yield at least one value')

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

    @override
    async def view(self) -> float:
        async with self.__lock:
            self.__state.ensure_could_view()
            time_left = self.__interval.time_left

            return time_left

    @override
    async def view_state(self) -> type[State]:
        async with self.__lock:
            return type(self.__state)

    async def __advance(self) -> None:
        try:
            while True:
                async with self.__lock:
                    self.__interval.advance()

                    if self.__interval.is_complete:
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

    def __make_interval_complete_event(self) -> IntervalCompleteEvent:
        event = IntervalCompleteEvent(
            timer=self,
            interval_number=self.__interval.number,
            interval_duration=self.__interval.duration,
        )

        return event

    def __make_timer_complete_event(self) -> TimerCompleteEvent:
        event = TimerCompleteEvent(
            timer=self,
            interval_count=self.__interval.number,
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
    def __validate_precision(cls, precision: float) -> None:
        if precision <= 0:
            raise InvalidPrecisionError
