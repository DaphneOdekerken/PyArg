from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.algorithms.semantics.get_admissible_sets import get_admissible_sets
from py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions
from py_arg.algorithms.semantics.get_eager_extension import get_eager_extension
from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension
from py_arg.algorithms.semantics.get_ideal_extension import get_ideal_extension
from py_arg.algorithms.semantics.get_preferred_extensions import get_preferred_extensions
from py_arg.algorithms.semantics.get_semistable_extensions import get_semistable_extensions
from py_arg.algorithms.semantics.get_stable_extensions import get_stable_extensions


def get_argumentation_framework_extensions(argumentation_framework: AbstractArgumentationFramework,
                                           semantics_specification: str):
    """
    Calculate the set of extensions from the given abstract argumentation framework and chosen semantics

    :param argumentation_framework: The abstract argumentation framework.
    :param semantics_specification: The chosen semantics.
    """
    if semantics_specification == 'Admissible':
        return get_admissible_sets(argumentation_framework)
    if semantics_specification == 'Complete':
        return get_complete_extensions(argumentation_framework)
    if semantics_specification == 'Grounded':
        return [get_grounded_extension(argumentation_framework)]
    if semantics_specification == 'Preferred':
        return get_preferred_extensions(argumentation_framework)
    if semantics_specification == 'Ideal':
        return get_ideal_extension(argumentation_framework)
    if semantics_specification == 'Stable':
        return get_stable_extensions(argumentation_framework)
    if semantics_specification == 'SemiStable':
        return get_semistable_extensions(argumentation_framework)
    if semantics_specification == 'Eager':
        return get_eager_extension(argumentation_framework)
