import pathlib


def path_to_resources():
    return pathlib.Path(__file__).parent.parent.parent / \
        'py_arg_tests' / 'resources'
