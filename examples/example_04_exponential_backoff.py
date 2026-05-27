from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.duration import exponentially, immediately_then
from aiotimer.event import ErrorEvent, IntervalCompleteEvent


async def main() -> None:
    """
    Demonstrate an example of an exponential backoff.
    """

    http_request_results = [False, False, False, True]
    http_request_result_iterator = iter(http_request_results)

    async def send_http_request(event: IntervalCompleteEvent) -> None:
        duration = event.interval_duration

        result = next(http_request_result_iterator)
        if not result:
            error = f'HTTP request failed after {duration} seconds.'
            raise RuntimeError(error)

        print(f'HTTP request succeeded after {duration} seconds.')
        await event.timer.reset()

    async def on_error(event: ErrorEvent) -> None:
        print(event.error)

    timer = Timer(
        immediately_then(exponentially(interval_count=3)),
        on_interval_complete=send_http_request,
        on_error=on_error,
    )
    await timer.start()
    print('The timer is running.')

    # Wait for the timer to complete.
    await sleep(7 + 0.1)


if __name__ == '__main__':
    run(main())
