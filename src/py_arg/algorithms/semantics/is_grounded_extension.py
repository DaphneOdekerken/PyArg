from typing import List

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension


def is_grounded_extension(argument_set: List[Argument], argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is the grounded extension in the corresponding argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is the grounded extension.
    :param argumentation_framework: Argumentation framework specifying defeats between arguments.
    :return: Is this argument set the grounded exension?

    >>> arguments = {s: Argument(s) for s in 'ABCD'}
    >>> defeats = [Defeat(arguments[s[0]], arguments[s[1]]) for s in ['AB', 'CC', 'BD']]
    >>> af = AbstractArgumentationFramework('Test', list(arguments.values()), defeats)
    >>> is_grounded_extension([arguments['A']], af)
    False
    >>> is_grounded_extension([arguments['D']], af)
    False
    >>> is_grounded_extension([arguments['A'], arguments['D']], af)
    True
    >>> is_grounded_extension([arguments['D'], arguments['A']], af)
    True
    """
    if any(argument not in argumentation_framework.arguments for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the argumentation framework.')

    sorted_grounded_extension = sorted(get_grounded_extension(argumentation_framework))
    sorted_set = sorted(argument_set)
    return sorted_grounded_extension == sorted_set
