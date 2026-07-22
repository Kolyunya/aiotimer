from pytest import mark

from aiotimer.utility.boolean import parse_boolean


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
