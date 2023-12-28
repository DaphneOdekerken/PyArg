from typing import List, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_grounded_extension \
    import get_grounded_extension

T = TypeVar('T', bound=Argument)


def is_grounded_extension(
        argument_set: List[T],
        argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is the grounded extension in the
    corresponding argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is
    the grounded extension.
    :param argumentation_framework: Argumentation framework specifying defeats
    between arguments.
    :return: Is this argument set the grounded extension?
    """
    if any(argument not in argumentation_framework.arguments
           for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the '
                         'argumentation framework.')

    sorted_grounded_extension = sorted(get_grounded_extension(
        argumentation_framework))
    sorted_set = sorted(argument_set)
    return sorted_grounded_extension == sorted_set
