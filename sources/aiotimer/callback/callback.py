from collections.abc import Awaitable
from inspect import isawaitable
from typing import Generic, Optional, cast

from ..event import EventType
from ..utility.function.has_parameters import has_parameters
from .user_callback import (
    ParameterizedUserCallback,
    ParameterlessUserCallback,
    UserCallback,
    UserCallbackResult,
)


class Callback(Generic[EventType]):

    def __init__(self, callback: UserCallback[EventType]) -> None:
        self.__callback = callback
        self.__has_parameters: Optional[bool] = None
        self.__is_asynchronous: Optional[bool] = None

        if callback:
            self.__has_parameters = has_parameters(callback)

            # We do not know if it is asynchronous before we call it.
            # And it is not time yet to call it.
            # We would find that out later after the first call.

    @property
    def is_set(self) -> bool:
        callback_is_set = self.__callback is not None
        return callback_is_set

    @property
    def is_missing(self) -> bool:
        callback_is_not_set = not self.is_set
        return callback_is_not_set

    async def __call__(self, event: EventType) -> None:
        if self.is_missing:
            return

        result = self.__invoke_callback(event)
        await self.__await_result(result)

    def __invoke_callback(self, event: EventType) -> UserCallbackResult:
        if self.__has_parameters:
            result = self.__parametrized_callback(event)
        else:
            result = self.__unparametrized_callback()

        return result

    async def __await_result(self, result: UserCallbackResult) -> None:
        if self.__is_asynchronous is None:
            self.__is_asynchronous = isawaitable(result)

        if self.__is_asynchronous is True:
            assert isinstance(result, Awaitable)
            await result

    @property
    def __parametrized_callback(self) -> ParameterizedUserCallback[EventType]:
        callback = cast(
            'ParameterizedUserCallback[EventType]',
            self.__callback,
        )

        return callback

    @property
    def __unparametrized_callback(self) -> ParameterlessUserCallback:
        callback = cast(
            'ParameterlessUserCallback',
            self.__callback,
        )

        return callback
