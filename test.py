import sys
from argparse import ArgumentParser
from os import environ
from subprocess import CalledProcessError, run

from aiotimer.utility.boolean import parse_boolean


def main() -> None:
    """Perform thorough quality assurance of the library code."""

    parser = ArgumentParser()
    parser.add_argument('--skip-slow', type=parse_boolean)
    arguments = parser.parse_args()

    marks = ''
    if arguments.skip_slow:
        marks = '(not slow)'

    environment = {
        **environ,
        'CLICOLOR': '1',
        'CLICOLOR_FORCE': '1',
        'FORCE_COLOR': '1',
    }

    sources = [
        'examples',
        'sources',
        'tests',
        'test.py',
    ]

    path = '.tools'
    commands = [
        ['ruff', f'--config={path}/ruff.toml', 'check', *sources],
        ['flake8', f'--config={path}/flake8.ini', *sources],
        ['pyright', f'--project={path}/pyright.json', *sources],
        ['mypy', f'--config-file={path}/mypy.ini', *sources],
        ['ty', 'check', f'--config-file={path}/ty.toml', *sources],
        ['pylint', f'--rcfile={path}/pylint.ini', *sources],
        ['pyrefly', 'check', f'--config={path}/pyrefly.toml'],
        ['pytest', f'--config-file={path}/pytest.ini', f'-m={marks}', 'tests'],
    ]

    success = True

    for command in commands:
        command_text = ' '.join(command)
        print(command_text)

        try:
            run(command, check=True, env=environment)
        except CalledProcessError:
            success = False

        print()

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
