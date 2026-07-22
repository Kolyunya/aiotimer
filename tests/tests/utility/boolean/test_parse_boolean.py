from pytest import mark, raises

from aiotimer.utility.boolean import parse_boolean


@mark.parametrize('string', [
    'yup',
    'nope',
    'maybe',
])
def test_unknow_values_raise_error(string: str) -> None:
    with raises(ValueError, match='Invalid boolean value'):
        parse_boolean(string)


@mark.parametrize('string', [
    '',
    '0',
    'n',
    'N',
    'no',
    'No',
    'false',
    'False',
])
def test_parses_as_false(string: str) -> None:
    boolean = parse_boolean(string)

    assert boolean is False


@mark.parametrize('string', [
    '1',
    'y',
    'Y',
    'yes',
    'Yes',
    'true',
    'True',
])
def test_parses_as_true(string: str) -> None:
    boolean = parse_boolean(string)

    assert boolean is True
