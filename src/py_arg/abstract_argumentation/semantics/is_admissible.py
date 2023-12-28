from typing import Iterable, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.is_acceptable_with_respect_to \
    import is_acceptable_with_respect_to
from py_arg.abstract_argumentation.semantics.is_conflict_free import \
    is_conflict_free

T = TypeVar('T', bound=Argument)


def is_admissible(
        argument_set: Iterable[T],
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

    if not is_conflict_free(argument_set, argumentation_framework):
        return False

    if any(not is_acceptable_with_respect_to(argument, argument_set,
                                             argumentation_framework)
           for argument in argument_set):
        return False

    return True
