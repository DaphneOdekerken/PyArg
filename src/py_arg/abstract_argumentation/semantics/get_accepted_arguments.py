from typing import FrozenSet, Set, TypeVar

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy

T = TypeVar('T', bound=Argument)


def get_accepted_arguments(
        extensions: Set[FrozenSet[T]],
        acceptance_strategy: AcceptanceStrategy) -> Set[T]:
    """
    Calculate the set of accepted arguments from a set of extensions
    (sets of arguments) and evaluation strategy

    :param extensions: The extensions (sets of collectively accepted arguments)
    :param acceptance_strategy: The acceptance strategy (e.g., skeptical or
    credulous).
    """
    if not extensions:
        return set()
    if acceptance_strategy == AcceptanceStrategy.SKEPTICAL:
        return set.intersection(*(set(argument_set)
                                  for argument_set in extensions))
    if acceptance_strategy == AcceptanceStrategy.CREDULOUS:
        return set.union(*(set(argument_set) for argument_set in extensions))
    raise NotImplementedError
