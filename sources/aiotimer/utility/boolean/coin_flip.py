from random import choice


def coin_flip() -> bool:
    """
    Return a uniformly distributed random boolean value.

    This function simulates a fair coin flip with equal probability
    of returning True (heads) or False (tails). The random
    distribution is uniform, ensuring no bias in the results.

    Returns:
        bool: True with 50% probability, False with 50% probability.

    Example:
        >>> # Simulate a coin flip
        >>> result = coin_flip()
        >>> print(f"Coin landed on {'heads' if result else 'tails'}")

    Note:
        Uses Python's random.choice() which provides cryptographically
        secure random number generation for applications requiring
        unpredictability.

    See Also:
        - random.choice: The underlying random function used.
    """

    coin_side = choice([
        True,
        False,
    ])

    return coin_side
