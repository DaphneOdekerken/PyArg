import itertools
from typing import Iterable, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat

T = TypeVar('T', bound=Argument)


def is_conflict_free(
        argument_set: Iterable[T],
        argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is conflict free in the corresponding
    argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is
    conflict-free.
    :param argumentation_framework: Argumentation framework specifying defeats
    between arguments.
    :return: Is this argument set conflict free?
    """
    if any(argument not in argumentation_framework.arguments
           for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the '
                         'argumentation framework.')

    return not any(Defeat(arg_a, arg_b) in argumentation_framework.defeats
                   for arg_a, arg_b in itertools.product(argument_set,
                                                         argument_set))
