from dataclasses import dataclass
from typing import TypeVar

from ..timer_interface import TimerInterface

EventType = TypeVar('EventType')


@dataclass(frozen=True)
class TimerEvent:

    timer: TimerInterface

    elapsed: float

    remaining: float
