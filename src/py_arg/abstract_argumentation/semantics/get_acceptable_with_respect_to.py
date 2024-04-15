from typing import Set, Iterable, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.is_acceptable_with_respect_to \
    import is_acceptable_with_respect_to

T = TypeVar('T', bound=Argument)


def get_acceptable_with_respect_to(
        argument_set: Iterable[T],
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[T]:
    """
    Get the set of argument that is acceptable with respect to this set of
    arguments.

    :param argument_set: The set of arguments for which we want to find the
        acceptable arguments.
    :param argumentation_framework: Abstract argumentation framework.
    :return: The set of arguments that are acceptable w.r.t. this set of
        arguments.
    """
    return {argument for argument in argumentation_framework.arguments
            if is_acceptable_with_respect_to(argument, argument_set,
                                             argumentation_framework)}
