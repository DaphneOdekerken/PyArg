import itertools
from typing import Iterable

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


def is_conflict_free(argument_set: Iterable[Argument], argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is conflict free in the corresponding argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is conflict-free.
    :param argumentation_framework: Argumentation framework specifying defeats between arguments.
    :return: Is this argument set conflict free?

    >>> arguments = {s: Argument(s) for s in 'ABC'}
    >>> defeats = [Defeat(arguments[s[0]], arguments[s[1]]) for s in ['AB', 'CC']]
    >>> af = AbstractArgumentationFramework('Test', list(arguments.values()), defeats)
    >>> is_conflict_free([arguments['C']], af)
    False
    >>> is_conflict_free([arguments['A']], af)
    True
    >>> is_conflict_free([arguments['A'], arguments['B']], af)
    False
    """
    if any(argument not in argumentation_framework.arguments for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the argumentation framework.')

    return not any(Defeat(arg_a, arg_b) in argumentation_framework.defeats
                   for arg_a, arg_b in itertools.product(argument_set, argument_set))
