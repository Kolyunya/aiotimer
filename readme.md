# Asyncio Timer

[![QA](https://github.com/Kolyunya/aiotimer/actions/workflows/qa.yaml/badge.svg)](https://github.com/Kolyunya/aiotimer/actions/workflows/qa.yaml) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Kolyunya_aiotimer&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Kolyunya_aiotimer) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Kolyunya_aiotimer&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Kolyunya_aiotimer) [![codecov](https://codecov.io/github/Kolyunya/aiotimer/graph/badge.svg?token=XTSKV4Q8CR)](https://codecov.io/github/Kolyunya/aiotimer)

An asynchronous timer with a human-friendly API and rich functionality.

* State management with `start()`, `stop()`, and `reset()` methods.
* On-the-fly duration adjustment with `prolong()`, `shorten()`, and `set()` methods.
* Introspection with `elapsed`, `remaining`, and `state` properties.
* Multi-interval timer configurations.
* Continuously running timers.
* Rich callback system enabling hooking into the timer lifecycle events.
* Synchronous and asynchronous callback execution modes.
* Concurrency-safe architecture designed to prevent race conditions and deadlocks.
* Support for a wide range of Python versions from `3.9` onward.
* Zero production dependencies except for [`typing-extensions`](https://github.com/python/typing_extensions) by the Python core team.

## Table of contents
* [Usage examples](#-usage-examples)
  * [One-off timer](#-one-off-timer)
  * [Multi-interval timer](#-multi-interval-timer)
  * [Other usage examples](#-other-usage-examples)
* [Public API](#-public-api)
  * [Controlling the state](#-controlling-the-state)
  * [Duration modification](#-duration-modification)
  * [Introspection](#-introspection)
* [States and transitions](#-states-and-transitions)
* [Configuring durations](#-configuring-durations)
  * [Single duration](#-single-duration)
  * [Sequence of durations](#-sequence-of-durations)
  * [Duration factory](#-duration-factory)
  * [Duration multipliers](#-duration-multipliers)
* [Event system](#-event-system)
  * [Interval complete event](#-interval-complete-event)
  * [Timer complete event](#-timer-complete-event)
  * [Error event](#-error-event)
* [Advanced usage](#-advanced-usage)
  * [Sync and Async callbacks](#-sync-and-async-callbacks)
  * [Configuring precision](#-configuring-precision)
  * [Custom duration factories](#-custom-duration-factories)
  * [Memory management](#-memory-management)
  * [Runtime type checking](#-runtime-type-checking)
* [Contributing](#-contributing)

## [🔝](#table-of-contents) Usage examples

### [🔝](#table-of-contents) One-off timer

A timer may have just one time interval.
```python
from asyncio import run, sleep

from aiotimer import Timer


async def main() -> None:
  """
  Will run the timer for 3 seconds.
  Then will print a message.
  """

  timer = Timer(3, lambda: print('3 seconds passed'))
  await timer.start()

  # Wait for the timer to complete.
  await sleep(3 + 1)


if __name__ == '__main__':
  run(main())
```

### [🔝](#table-of-contents) Multi-interval timer

A timer may have multiple time intervals of arbitrary durations.
```python
from asyncio import run, sleep

from aiotimer import Timer
from aiotimer.duration.factory import thrice
from aiotimer.duration.multiplier import second


async def main() -> None:
  """
  Will run the timer three times for 1 second each.
  And will print intermediate messages every second.
  Then will print the final message after a total of 3 seconds.
  """

  timer = Timer(
    thrice(1 * second),
    lambda: print('3 seconds passed'),
    lambda: print('1 more second passed'),
  )
  await timer.start()

  # Wait for the timer to complete.
  await sleep(3 + 1)


if __name__ == '__main__':
  run(main())
```

### [🔝](#table-of-contents) Other usage examples
More usage examples are available [here](examples).

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>

## [🔝](#table-of-contents) Public API

### [🔝](#table-of-contents) Controlling the state
* `await timer.start()` starts the timer that is in the `Initial` or in the `Stopped` state.
* `await timer.stop()` stops the timer that is in the `Running` state. The elapsed and remaining times for the current time interval as well as the current interval itself are **_preserved_**.
* `await timer.reset()` resets the timer. The elapsed and remaining times for the current time interval as well as the current interval itself are **_discarded_**. The timer is reset to the initial state it had after instantiation.

### [🔝](#table-of-contents) Duration modification
* `await timer.set(duration)` sets the duration of the currently running interval **_to_** `duration`. In case the elapsed time is greater than `duration`, the interval would complete immediately.
* `await timer.prolong(delta)` prolongs the duration of the currently running interval **_by_** `delta`.
* `await timer.shorten(delta)` shortens the duration of the currently running interval **_by_** `delta`. In case the elapsed time is greater than the resulting duration after shortening, the interval would complete immediately.

### [🔝](#table-of-contents) Introspection
* `timer.elapsed` returns the elapsed time for the currently running interval.
* `timer.remaining` returns the remaining time for the currently running interval.
* `timer.state` returns the type of the current state of the timer.

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>

## [🔝](#table-of-contents) States and transitions
The timer class implements the [State Pattern](https://en.wikipedia.org/wiki/State_pattern). Methods that modify the timer state may only be called when the timer is in a supported state.

Any transition not listed in the diagram will raise an [`InvalidStateError`](sources/aiotimer/error/state_error.py). For example, you cannot `reset()` a timer while it is in the `InitialState`, and you cannot `start()` a timer that is in the `CompleteState`.

This design is used as a defensive programming technique that helps catch any logic errors in the code early and simplifies the debugging process.

![](.assets/state-diagram.png)

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>

## [🔝](#table-of-contents) Configuring durations
The first parameter of the timer constructor defines its interval durations. A timer may have one or more time intervals of arbitrary durations, all measured in seconds. The parameter accepts three different forms, from the simplest to the most powerful:

* [A single duration](#-single-duration) — for one-off timers with a single interval.
* [A sequence of durations](#-sequence-of-durations) — for timers with a fixed, known set of intervals.
* [A duration factory](#-duration-factory) — for complex duration generation logic.

> All interval durations **_must_** be positive numbers or zeroes, regardless of the form used. A negative duration yields an undefined behavior.

> Duration objects **_must not_** be modified after they are passed to a timer, regardless of the form used. Modifying them yields an undefined behavior.

### [🔝](#table-of-contents) Single duration
This is the simplest duration form for one-off timers. Any integer or floating-point number configures a timer with exactly one interval of the given duration in seconds.

```python
from aiotimer import Timer


# A one-off timer with a single 5-second interval.
Timer(5, lambda: print('Timer complete'))
```

### [🔝](#table-of-contents) Sequence of durations
This is the most convenient duration form when the set of intervals is static and known upfront. Any [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence) of durations (e.g. a list or a tuple) configures a multi-interval timer.

```python
from aiotimer import Timer


# Three intervals of 1, 2, and 3 seconds.
Timer(
  [1, 2, 3],
  lambda: print('Timer complete'),
  lambda: print('Interval complete'),
)


# Same as previous, but using a tuple.
Timer(
  (1, 2, 3),
  lambda: print('Timer complete'),
  lambda: print('Interval complete'),
)
```

> A duration sequence **_must not_** be empty. An empty sequence raises an [`EmptyDurationIterableError`](sources/aiotimer/error/duration_error.py).

### [🔝](#table-of-contents) Duration factory
This is the most powerful form of durations. A [`Duration Factory`](sources/aiotimer/duration/factory) is a callable that returns an `Iterable` of durations. It powers more complex duration generation logic as well as infinitely-running timers.

The library is shipped with an extensive catalog of built-in duration factories that should cover the majority of common use cases. Also see [Custom duration factories](#-custom-duration-factories) for implementing your own factory.

```python
from aiotimer.duration.factory import *


# Generates 1 interval of 5 seconds.
once(5)


# Generates 2 intervals of 5 seconds each.
twice(5)


# Generates 3 intervals of 5 seconds each.
thrice(5)


# Generates 10 intervals of 5 seconds each.
repeatedly(5, 10)


# Generates 3 intervals of 1, 2, and 3 seconds.
sequentially(1, 2, 3)


# Generates an infinite number of 5-second intervals.
forever(5)


# Generates 1 interval between 5 and 10 seconds.
randomly(5, 10)


# Generates 3 intervals of 5±0.5 seconds (10% relative jitter).
# Any other factory may be passed as the first argument.
jittery(thrice(5), relative=0.1)


# Generates 3 intervals of 5±0.5 seconds (0.5 second absolute jitter).
# Any other factory may be passed as the first argument.
jittery(thrice(5), absolute=0.5)


# Generates 5 intervals of 1, 2, 4, 8, and 16 seconds.
exponentially(interval_count=5)


# Same as previous but limited by the duration instead.
exponentially(maximum_duration=16)


# Generates faster-growing intervals of 1, 3, and 9 seconds.
exponentially(base=3, interval_count=3)


# Generates scaled-down intervals of 0.1, 0.2, and 0.4 seconds.
exponentially(scale=0.1, interval_count=3)


# Generates a zero-second interval followed by 5 exponentially growing retries.
# Retry delays are powers of 2, each divided by 2 with a ±25% jitter applied.
# Resulting durations are 0, 0.5±25%, 1±25%, 2±25%, 4±25%, and 8±25%.
backoff()


# Generates more retries.
backoff(retries=10)


# Stops retry generation after reaching the maximum duration.
# Jitter is excluded from the calculation.
backoff(maximum_duration=60)


# Applies a faster exponential growth.
backoff(base=3)


# Applies a stronger down-scaling.
backoff(scale=0.1)


# Applies a lighter jitter.
backoff(jitter=0.1)


# Generates 4 intervals of 0, 5, 5, and 5 seconds.
# Any other factory may be passed as the first argument.
immediately_then(thrice(5))
```

> If you believe some type of duration factory is missing, feel free to submit an issue or a pull request.

All factories that wrap another duration source (`once`, `twice`, `thrice`, `repeatedly`, `sequentially`, `forever`, `jittery`, `immediately_then`) accept all three forms of durations. This enables a very powerful mechanism of factory composition. A few examples are listed below.

```python
from aiotimer.duration.factory import *


# Generates 9 intervals with a repeating pattern of 1, 2, and 3 seconds.
thrice([1, 2, 3])


# Generates 10 intervals between 5 and 10 seconds each.
repeatedly(randomly(5, 10), 10)


# Generates a random interval followed by an exponential sequence.
sequentially(
  randomly(0.1, 0.2),
  exponentially(interval_count=10),
)


# Generates 10 exponentially-growing intervals with a 10% jitter applied to them.
jittery(exponentially(interval_count=10), relative=0.1)


# Generates an infinite number of intervals of 1, 2, 3, 1, 2, 3, ... seconds.
# Any other factory may be passed as the first argument.
forever(sequentially(1, 2, 3))
```

### [🔝](#table-of-contents) Duration multipliers
A timer always expects durations to be passed in seconds (`float` or `int`). To express durations in other time units conveniently, the library ships a set of [duration multipliers](sources/aiotimer/duration/multiplier) — plain numeric constants that scale duration values into seconds.

```python
from aiotimer.duration.multiplier import *


millisecond, milliseconds  # 0.001
second, seconds            # 1
minute, minutes            # 60
hour, hours                # 3600
day, days                  # 86400
week, weeks                # 604800
month, months              # 2592000 (30 days)
year, years                # 31536000 (365 days)
```

Each multiplier is available in both a singular and a plural form. The two are interchangeable. You may pick whichever reads more naturally.

```python
from aiotimer import Timer
from aiotimer.duration.factory import thrice
from aiotimer.duration.multiplier import hour, milliseconds, minutes, seconds

# A single 5-minute interval.
Timer(5 * minutes)

# Three intervals of 30 seconds, 5 minutes, and 1 hour.
Timer([30 * seconds, 5 * minutes, 1 * hour])

# Three 100-millisecond intervals.
Timer(thrice(100 * milliseconds))
```

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>

## [🔝](#table-of-contents) Event system
There are several event handlers that may be configured for a timer through the constructor arguments.

All event handlers **_must_** comply with the following API contract. Non-compliant event handlers result in undefined behavior.
* Event handler **_must_** have either:
    * Zero parameters.
    * Exactly one positional parameter accepting the corresponding event object type.
* An event handler's signature **_must not_** be modified at runtime after registration with the timer object.
* Event handler **_should not_** return any values because they will be ignored and discarded by the timer.
* Event handler **_may_** be either:
  * Synchronous callable.
  * Asynchronous callable.

> All event objects have a `timer` property that references the timer object that fired the event.

> Any public method of a timer object may be safely called from any event handler. The internal timer architecture prevents any race conditions and deadlocks from occurring.

### [🔝](#table-of-contents) Interval complete event
This event is fired each time any interval of a timer is complete. An `on_interval_complete` handler **_may_** optionally accept an [`IntervalCompleteEvent`](sources/aiotimer/event/interval_complete_event.py) object. Events of this type have the following properties:
* `timer: Timer`
* `interval_number: int`
* `interval_duration: float`

### [🔝](#table-of-contents) Timer complete event
This event is fired each time the last interval of a timer is complete. An `on_timer_complete` handler **_may_** optionally accept a [`TimerCompleteEvent`](sources/aiotimer/event/timer_complete_event.py) object. Events of this type have the following properties:
* `timer: Timer`
* `interval_count: int`

### [🔝](#table-of-contents) Error event
This event is fired each time any exception is propagated from any of the event handlers described above. Additionally, it is fired when an exception occurs inside a system coroutine of a timer. An `on_error` handler **_may_** optionally accept an [`ErrorEvent`](sources/aiotimer/event/error_event.py) object. Events of this type have the following properties:
* `timer: Timer`
* `error: Exception`

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>

## [🔝](#table-of-contents) Advanced usage

### [🔝](#table-of-contents) Sync and Async callbacks
Use the `await_callbacks` parameter of the `Timer` constructor to control the way the callbacks are handled.

In the sync mode (`await_callbacks == True`) the next interval would not start until the `on_interval_complete` callback finishes execution.

In the async mode (`await_callbacks == False`) the next interval would start immediately after the previous one completes.

> Both modes support `def`, `async def` as well as any other types of [compatible callables](#-event-system). It's perfectly fine to use `def` in the async mode and `async def` in sync mode.

### [🔝](#table-of-contents) Configuring precision
The timer class has a configurable `precision: float` parameter. It represents the number of seconds a timer would idle between its system ticks.

For adequate accuracy, it is recommended to have the precision value configured significantly (at least several times) smaller than the shortest interval the timer would have.

At the same time, having the precision configured to an extremely low value (e.g. `0.001`) may yield a high CPU load.

### [🔝](#table-of-contents) Custom duration factories
A [`Duration Factory`](sources/aiotimer/duration/duration.py) is one of the three forms the timer constructor accepts for its first argument (see [Configuring durations](#-configuring-durations)). It is a callable that returns an `Iterable` of durations.

In case the [built-in factories](#-duration-factory) do not cover your usage scenarios, you can construct your custom one. The simplest custom duration factory is a `lambda` returning a list of durations.

```python
from asyncio import run, sleep

from aiotimer import Timer


async def main() -> None:
  duration_factory = lambda: [1, 2, 3]

  timer = Timer(
    duration_factory,
    lambda: print('6 seconds passed'),
  )

  await timer.start()

  # Wait for the timer to complete.
  await sleep(6 + 1)


if __name__ == '__main__':
  run(main())
```

### [🔝](#table-of-contents) Memory management
A timer in the `Running` state will never be garbage-collected, nor will event handlers registered with it. They are referenced by the event loop and live at least until the timer is stopped.

Inherently infinitely-running timers must be stopped manually as soon as they are no longer needed. Failing to do so effectively results in a memory leak.

### [🔝](#table-of-contents) Runtime type checking
The library supports optional runtime type checking of its whole codebase powered by [`beartype`](https://beartype.readthedocs.io/).

To enable it, install `beartype` and set the `BEARTYPE` environment variable to any truthy value (e.g. `Yes`, `True`, `1`) before importing the library.

```bash
pip install beartype
BEARTYPE=Yes python main.py
```

> The variable name intentionally does not have a library prefix, so that a single switch can enable runtime type checking across every library and application following the same convention.

In case the variable is set but `beartype` is not installed, the library emits a warning and runs normally, just with type checking disabled.

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>

## [🔝](#table-of-contents) Contributing

### [🔝](#table-of-contents) Configuring the development environment
```bash
# Create and activate a virtual environment.
python -m venv .
source bin/activate

# Install the library and its dependencies.
pip install --upgrade pip
pip install --editable ".[development]"

# Run the test suite.
BEARTYPE=Yes python -m test --skip-slow=No
```

Additionally, convenient `Quick QA` and `Full QA` run configurations are provided for `PyCharm` users.

<div align="right">

**[🔝 Back to top](#table-of-contents)**

</div>
