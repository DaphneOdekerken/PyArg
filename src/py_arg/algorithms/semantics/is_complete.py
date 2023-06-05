from typing import List

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.semantics.get_acceptable_with_respect_to import get_acceptable_with_respect_to
from py_arg.algorithms.semantics.is_admissible import is_admissible


def is_complete(argument_set: List[Argument], argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is admissible in the corresponding argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is admissible.
    :param argumentation_framework: Argumentation framework specifying defeats between arguments.
    :return: Is this argument set admissible?

    >>> arguments = {s: Argument(s) for s in 'ABCD'}
    >>> defeats = [Defeat(arguments[s[0]], arguments[s[1]]) for s in ['AB', 'BA', 'AC', 'BC', 'CD']]
    >>> af = AbstractArgumentationFramework('Test', list(arguments.values()), defeats)
    >>> is_complete([arguments['C']], af)
    False
    >>> is_complete([arguments['A']], af)
    False
    >>> is_complete([arguments['B']], af)
    False
    >>> is_complete([arguments['A'], arguments['B']], af)
    False
    >>> is_complete([arguments['D']], af)
    False
    >>> is_complete([arguments['A'], arguments['D']], af)
    True
    >>> is_complete([arguments['B'], arguments['D']], af)
    True
    """
    if any(argument not in argumentation_framework.arguments for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the argumentation framework.')

    if not is_admissible(argument_set, argumentation_framework):
        return False

    if any(acceptable_argument not in argument_set
           for acceptable_argument in get_acceptable_with_respect_to(argument_set, argumentation_framework)):
        return False

    return True
