from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.event import ErrorEvent, IntervalCompleteEvent
from aiotimer.interval import exponentially, immediately_then


async def main() -> None:
    """
    Demonstrate an example of an exponential backoff.
    """

    http_request_results = [False, False, False, True]
    http_request_result_generator = (
        success for success in http_request_results
    )

    async def send_http_request(event: IntervalCompleteEvent) -> None:
        duration = event.interval_duration

        result = next(http_request_result_generator)
        if not result:
            error = f'HTTP request failed after {duration} seconds.'
            raise RuntimeError(error)

        print(f'HTTP request succeeded after {duration} seconds.')
        await event.timer.pause()

    async def on_error(event: ErrorEvent) -> None:
        print(event.error)

    timer = Timer(
        immediately_then(exponentially(intervals=10)),
        on_interval_complete=send_http_request,
        on_error=on_error,
    )
    await timer.run()
    print('The timer is running.')

    # Add a sleep margin of one second to avoid any race conditions.
    await sleep(10)


if __name__ == '__main__':
    run(main())
