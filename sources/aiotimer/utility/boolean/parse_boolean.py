def parse_boolean(string: str) -> bool:
    """
    Parse a string representation of a boolean value.

    This function converts an explicit set of string representations of
    boolean values to their corresponding boolean equivalents, matching
    case-insensitively. Any string outside these sets is rejected.

    Args:
        string: The string to parse. Recognized values (case-insensitive):
                truthy: 'true', 'yes', 'y', '1'
                falsy:  'false', 'no', 'n', '0', '' (empty string)

    Returns:
        bool: True for a truthy value, False for a falsy value.

    Raises:
        ValueError: If the string is not a recognized truthy or falsy value.

    Example:
        >>> # Parse various boolean representations.
        >>> parse_boolean('true')    # Returns True
        >>> parse_boolean('YES')     # Returns True
        >>> parse_boolean('false')   # Returns False
        >>> parse_boolean('no')      # Returns False
        >>> parse_boolean('maybe')   # Raises ValueError

    Note:
        Only explicitly recognized values are accepted. Unlike a permissive
        parser, unrecognized input raises ValueError rather than silently
        defaulting to True or False.
    """

    truthy = [
        'true',
        'yes',
        'y',
        '1',
    ]

    falsy = [
        'false',
        'no',
        'n',
        '0',
        '',
    ]

    string = string.lower()

    if string in truthy:
        is_truthy = True
    elif string in falsy:
        is_truthy = False
    else:
        raise ValueError('Invalid boolean value')

    return is_truthy
