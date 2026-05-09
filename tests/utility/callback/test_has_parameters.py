from aiotimer.utility.callback import has_parameters


def test_function_has_no_parameters() -> None:
    def function() -> None:
        pass

    result = has_parameters(function)

    assert result is False


def test_function_has_positional_parameter() -> None:
    def function(parameter: str) -> str:
        return parameter

    result = has_parameters(function)

    assert result is True


def test_function_has_multiple_positional_parameters() -> None:
    def function(parameter_one: str, parameter_two: str) -> str:
        return parameter_one + parameter_two

    result = has_parameters(function)

    assert result is True


def test_function_has_variable_positional_parameters() -> None:
    def function(*parameters: str) -> tuple[str, ...]:
        return parameters

    result = has_parameters(function)

    assert result is True


def test_function_has_variable_keyword_parameters() -> None:
    def function(**parameters: str) -> dict[str, str]:
        return parameters

    result = has_parameters(function)

    assert result is True
