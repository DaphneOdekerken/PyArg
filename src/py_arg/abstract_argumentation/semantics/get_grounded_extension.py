from typing import Set, FrozenSet, TypeVar

from py_arg.abstract_argumentation.semantics.get_acceptable_with_respect_to \
    import get_acceptable_with_respect_to
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.utils.fixpoint import get_least_fixed_point

T = TypeVar('T', bound=Argument)


def get_grounded_extension(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[T]:
    return get_least_fixed_point(
        lambda x: get_acceptable_with_respect_to(x, argumentation_framework),
        set())


def get_grounded_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    return {frozenset(get_grounded_extension(argumentation_framework))}
