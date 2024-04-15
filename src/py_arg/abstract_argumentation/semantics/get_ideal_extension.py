from typing import Set, TypeVar, FrozenSet

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_admissible_sets import \
    get_admissible_sets
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    get_preferred_extensions

T = TypeVar('T', bound=Argument)


def get_ideal_extension(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[T]:
    """
    Get the ideal extension of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
        need the ideal extension.
    :return: ideal extension of the argumentation framework.
    """
    admissible_sets = get_admissible_sets(argumentation_framework)
    preferred_extensions = get_preferred_extensions(argumentation_framework)
    preferred_extension_sets = (set(ext) for ext in preferred_extensions)

    intersect_preferred = set.intersection(*preferred_extension_sets)

    max_admissible_subset_of_preferred = None
    for candidate_ideal_extension in admissible_sets:
        if candidate_ideal_extension <= intersect_preferred:
            if not max_admissible_subset_of_preferred:
                max_admissible_subset_of_preferred = candidate_ideal_extension
            if candidate_ideal_extension > max_admissible_subset_of_preferred:
                max_admissible_subset_of_preferred = candidate_ideal_extension

    return set(max_admissible_subset_of_preferred)


def get_ideal_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    return {frozenset(get_ideal_extension(argumentation_framework))}
