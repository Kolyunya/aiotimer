from aiotimer.utility.function import has_parameters


def test_function_has_no_parameters() -> None:
    def function() -> None:
        pass

    result = has_parameters(function)

    assert result is False


def test_function_has_positional_parameter() -> None:
    def function(_: str) -> None:
        pass

    result = has_parameters(function)

    assert result is True


def test_function_has_multiple_positional_parameters() -> None:
    def function(_: str, __: str) -> None:
        pass

    result = has_parameters(function)

    assert result is True


def test_function_has_variable_positional_parameters() -> None:
    def function(*_: str) -> None:
        pass

    result = has_parameters(function)

    assert result is True


def test_function_has_variable_keyword_parameters() -> None:
    def function(**_: str) -> None:
        pass

    result = has_parameters(function)

    assert result is True
