NANOSECONDS_IN_SECOND = 1_000_000_000


def s2ns(seconds: float) -> int:
    """
    Convert seconds to nanoseconds.

    Args:
        seconds: The duration in seconds to convert.

    Returns:
        int: The equivalent duration in nanoseconds (rounded to nearest integer).

    Example:
        >>> # Convert various time durations.
        >>> s2ns(1.0)        # Returns 1_000_000_000
        >>> s2ns(0.5)        # Returns 500_000_000
        >>> s2ns(0.001)      # Returns 1_000_000

    Note:
        Result is rounded to the nearest nanosecond.

    See Also:
        - ns2s: The inverse conversion function
    """

    nanoseconds_float = seconds * NANOSECONDS_IN_SECOND
    nanoseconds_int = round(nanoseconds_float)

    return nanoseconds_int


def ns2s(nanoseconds: int) -> float:
    """
    Convert nanoseconds to seconds.

    Args:
        nanoseconds: The duration in nanoseconds to convert.

    Returns:
        float: The equivalent duration in seconds.

    Example:
        >>> # Convert various time durations
        >>> ns2s(1_000_000_000)  # Returns 1.0
        >>> ns2s(500_000_000)    # Returns 0.5
        >>> ns2s(1_000_000)      # Returns 0.001

    See Also:
        - s2ns: The inverse conversion function
    """

    seconds = nanoseconds / NANOSECONDS_IN_SECOND

    return seconds
