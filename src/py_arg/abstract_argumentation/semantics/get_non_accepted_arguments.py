from typing import FrozenSet, Set, TypeVar

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy
from py_arg.abstract_argumentation.semantics.get_accepted_arguments import \
    get_accepted_arguments

T = TypeVar('T', bound=Argument)


def get_non_accepted_arguments(
        original_arguments: Set[T],
        extensions: Set[FrozenSet[T]],
        acceptance_strategy: AcceptanceStrategy) -> \
        Set[T]:
    """
    Calculate the set of non-accepted arguments from a set of extensions
    (sets of arguments) and evaluation strategy

    :param original_arguments: All arguments in the argumentation framework.
    :param extensions: The extensions (sets of collectively accepted arguments)
    :param acceptance_strategy: The acceptance strategy (e.g., skeptical or
    credulous).
    """
    accepted_arguments = get_accepted_arguments(
        extensions, acceptance_strategy)
    return original_arguments.difference(accepted_arguments)
