import itertools
from typing import List

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.semantics.is_admissible import is_admissible


def is_preferred_extension(argument_set: List[Argument], argumentation_framework: AbstractArgumentationFramework) \
        -> bool:
    """
    Check if the argument set if it is a preferred extension in the corresponding argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is a preferred extension.
    :param argumentation_framework: Argumentation framework specifying defeats between arguments.
    :return: Is this argument set a preferred exension?

    >>> arguments = {s: Argument(s) for s in 'ABCDEF'}
    >>> defeats = [Defeat(arguments[s[0]], arguments[s[1]]) for s in ['AB', 'CC', 'BD', 'EF', 'FE']]
    >>> af = AbstractArgumentationFramework('Test', list(arguments.values()), defeats)
    >>> is_preferred_extension([arguments['A'], arguments['D']], af)
    False
    >>> is_preferred_extension([arguments['D'], arguments['A']], af)
    False
    >>> is_preferred_extension([arguments['E']], af)
    False
    >>> is_preferred_extension([arguments['A'], arguments['D'], arguments['E']], af)
    True
    >>> is_preferred_extension([arguments['D'], arguments['A'], arguments['E']], af)
    True
    >>> is_preferred_extension([arguments['A'], arguments['D'], arguments['F']], af)
    True
    >>> is_preferred_extension([arguments['D'], arguments['A'], arguments['F']], af)
    True
    """
    if any(argument not in argumentation_framework.arguments for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the argumentation framework.')

    if not is_admissible(argument_set, argumentation_framework):
        return False

    # Iterator for generating all sets of arguments
    arguments_not_in_argument_set = [arg for arg in argumentation_framework.arguments if arg not in argument_set]
    all_combinations_of_arguments_not_in_argument_set = itertools.chain.from_iterable(
        itertools.combinations(arguments_not_in_argument_set, n)
        for n in range(1, len(arguments_not_in_argument_set) + 1))
    if any(is_admissible(argument_set + list(subset), argumentation_framework)
           for subset in all_combinations_of_arguments_not_in_argument_set):
        return False

    return True
