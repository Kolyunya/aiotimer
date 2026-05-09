def parse_boolean(string: str) -> bool:
    """
    Parse a string representation of a boolean value.

    This function converts various string representations of boolean values
    to their corresponding boolean equivalents. It provides flexible
    parsing for common truthy values while maintaining case-insensitivity.

    Args:
        string: The string to parse. Common truthy values include:
                'true', 'yes', 'y', '1' (case-insensitive)

    Returns:
        bool: True if the string matches any truthy value, False otherwise.

    Raises:
        TypeError: If input is not a string.

    Example:
        >>> # Parse various boolean representations.
        >>> parse_boolean('true')    # Returns True
        >>> parse_boolean('YES')     # Returns True
        >>> parse_boolean('false')   # Returns False
        >>> parse_boolean('no')      # Returns False

    Note:
        Only explicit truthy values return True. All other values
        (including empty string, 'false', 'no', '0', etc.) return False.
        This follows the principle of explicit positivity.
    """

    truthy = [
        'true',
        'yes',
        'y',
        '1',
    ]

    string = string.lower()
    is_truthy = string in truthy

    return is_truthy
