from collections.abc import Callable
from inspect import signature
from typing import Any


def has_parameters(the_callable: Callable[..., Any]) -> bool:
    """
    Check if a callable accepts any parameters.

    This function inspects the signature of a callable to determine
    whether it accepts any parameters. It's used for determining whether
    to invoke user callbacks with or without arguments.

    Args:
        the_callable: The callable to inspect for parameter requirements.

    Returns:
        bool: True if the callable accepts one or more parameters,
               False if it accepts no parameters.

    Example:
        >>> # Functions with parameters.
        >>> def func_with_args(x, y): pass
        >>> has_parameters(func_with_args)  # Returns True

        >>> # Functions without parameters.
        >>> def func_no_args(): pass
        >>> has_parameters(func_no_args)   # Returns False

        >>> # Lambda functions
        >>> has_parameters(lambda x: x)    # Returns True
        >>> has_parameters(lambda: None)   # Returns False

    Note:
        Uses Python's inspect.signature() to analyze callable signatures.
        This works with regular functions, methods, lambda functions,
        and any other callable objects that support introspection.

    Raises:
        ValueError: If the callable's signature cannot be inspected
                  (rare, typically with built-in functions).

    See Also:
        - inspect.signature: The underlying inspection function used
    """

    the_signature = signature(the_callable)

    parameters_count = len(the_signature.parameters)
    callable_has_parameters = parameters_count > 0

    return callable_has_parameters
