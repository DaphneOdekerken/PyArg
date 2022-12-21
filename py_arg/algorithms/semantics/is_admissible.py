from typing import Iterable

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.semantics.is_acceptable_with_respect_to import is_acceptable_with_respect_to
from py_arg.algorithms.semantics.is_conflict_free import is_conflict_free


def is_admissible(argument_set: Iterable[Argument], argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is admissible in the corresponding argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is admissible.
    :param argumentation_framework: Argumentation framework specifying defeats between arguments.
    :return: Is this argument set admissible?

    >>> arguments = {s: Argument(s) for s in 'ABCD'}
    >>> defeats = [Defeat(arguments[s[0]], arguments[s[1]]) for s in ['AB', 'BA', 'AC', 'BC', 'CD']]
    >>> af = AbstractArgumentationFramework('Test', list(arguments.values()), defeats)
    >>> is_admissible([arguments['C']], af)
    False
    >>> is_admissible([arguments['A']], af)
    True
    >>> is_admissible([arguments['B']], af)
    True
    >>> is_admissible([arguments['A'], arguments['B']], af)
    False
    >>> is_admissible([arguments['D']], af)
    False
    >>> is_admissible([arguments['A'], arguments['D']], af)
    True
    >>> is_admissible([arguments['B'], arguments['D']], af)
    True
    """
    if any(argument not in argumentation_framework.arguments for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the argumentation framework.')

    if not is_conflict_free(argument_set, argumentation_framework):
        return False

    if any(not is_acceptable_with_respect_to(argument, argument_set, argumentation_framework)
           for argument in argument_set):
        return False

    return True
