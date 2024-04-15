from typing import TypeVar, Callable

T = TypeVar('T')


def get_least_fixed_point(function: Callable[[T], T], function_input: T) -> T:
    """
    Get the least fixed point of a given function, by applying this function
    until the result did not change anymore.

    :param function: The function that should be applied iteratively.
    :param function_input: Initial input.
    :return: Least fixed point output.

    >>> get_least_fixed_point(lambda x: min(x + 1, 5), 0)
    5
    >>> get_least_fixed_point(lambda x: x[1:], ['a', 'b', 'c'])
    []

    """
    def copy_function(x):
        if hasattr(function_input, '__copy__'):
            return x.__copy__()
        return x

    previous_output = copy_function(function_input)
    new_output = function(previous_output)
    while previous_output != new_output:
        previous_output = copy_function(new_output)
        new_output = function(previous_output)
    return new_output


if __name__ == "__main__":
    import doctest

    doctest.testmod()
