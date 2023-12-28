from typing import Set, TypeVar, FrozenSet

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_admissible_sets import \
    get_admissible_sets
from py_arg.abstract_argumentation.semantics.get_semistable_extensions import \
    get_semi_stable_extensions

T = TypeVar('T', bound=Argument)


def get_eager_extension(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[T]:
    """
    Get the eager extension of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
        need the eager extension.
    :return: eager extension of the argumentation framework.
    """
    admissible_sets = get_admissible_sets(argumentation_framework)
    semi_stable_extensions = get_semi_stable_extensions(
        argumentation_framework)
    semi_stable_extension_sets = (set(ext) for ext in semi_stable_extensions)

    intersect_semi_stable = set.intersection(*semi_stable_extension_sets)

    max_admissible_subset_of_semi_stable = None
    for candidate_eager in admissible_sets:
        if candidate_eager <= intersect_semi_stable:
            if not max_admissible_subset_of_semi_stable:
                max_admissible_subset_of_semi_stable = candidate_eager
            if candidate_eager > max_admissible_subset_of_semi_stable:
                max_admissible_subset_of_semi_stable = candidate_eager

    return set(max_admissible_subset_of_semi_stable)


def get_eager_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    return {frozenset(get_eager_extension(argumentation_framework))}
