from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock

from aiotimer.event import TimerEvent


@dataclass(frozen=True)
class EventData:
    event: type[TimerEvent]
    data: dict[str, Any]


def assert_callback_awaited(mock: AsyncMock, awaits: list[EventData]) -> None:
    assert mock.await_count == len(awaits)

    actual_awaits = enumerate(mock.await_args_list)
    for await_index, await_data in actual_awaits:
        event = await_data.args[0]
        assert isinstance(event, awaits[await_index].event)

        for argument, value in awaits[await_index].data.items():
            actual_value = getattr(event, argument)
            assert actual_value == value
