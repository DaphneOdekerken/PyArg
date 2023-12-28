from typing import List, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_acceptable_with_respect_to \
    import get_acceptable_with_respect_to
from py_arg.abstract_argumentation.semantics.is_admissible import is_admissible

T = TypeVar('T', bound=Argument)


def is_complete(
        argument_set: List[T],
        argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Check if the argument set if it is admissible in the corresponding
    argumentation framework.
    :param argument_set: Set of arguments for which we want to know if it is
    admissible.
    :param argumentation_framework: Argumentation framework specifying defeats
    between arguments.
    :return: Is this argument set admissible?
    """
    if any(argument not in argumentation_framework.arguments
           for argument in argument_set):
        raise ValueError('Not all arguments in the argument set are in the '
                         'argumentation framework.')

    if not is_admissible(argument_set, argumentation_framework):
        return False

    if any(acceptable_argument not in argument_set
           for acceptable_argument in get_acceptable_with_respect_to(
                argument_set, argumentation_framework)):
        return False

    return True
