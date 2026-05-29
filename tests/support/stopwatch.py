from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Optional


@dataclass
class __Time:
    elapsed: Optional[float]


@asynccontextmanager
async def stopwatch() -> AsyncGenerator[__Time, None]:
    time_start = perf_counter()

    result = __Time(None)

    try:
        yield result
    finally:
        time_end = perf_counter()
        result.elapsed = time_end - time_start
