from asyncio import Event, run, sleep

from tests.support import stopwatch

from aiotimer import Timer
from aiotimer.duration.factory import thrice


async def main() -> None:
    """
    Demonstrate an example of a timer that does not await callbacks.

    Note that the timer keeps running, while the `on_interval_complete`
    callback is sleeping. The timer is not waiting for it to complete.
    """

    async def on_timer_complete() -> None:
        timer_is_complete.set()

    async def on_interval_complete() -> None:
        await sleep(1)

    timer = Timer(
        thrice(1),
        on_timer_complete,
        on_interval_complete,
        await_callbacks=False,
    )

    timer_is_complete = Event()

    async with stopwatch() as time:
        print('The timer is running.')
        await timer.start()
        await timer_is_complete.wait()

    print(f'The timer is complete in {time.elapsed:.3f} seconds.')


if __name__ == '__main__':
    run(main())
