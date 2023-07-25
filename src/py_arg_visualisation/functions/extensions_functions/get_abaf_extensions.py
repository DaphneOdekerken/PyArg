from py_arg.aba_classes.aba_framework import ABAF
import py_arg.aba_classes.semantics.get_stable_extensions as get_stable_extensions
from src import py_arg as get_preferred_extensions, py_arg as get_naive_extensions, py_arg as get_admissible_extensions
import py_arg as get_complete_extensions
import py_arg as get_semi_stable_extensions
import py_arg as get_ground_extensions
import py_arg.aba_classes.semantics.get_conflict_free_extensions as get_conflict_free_extensions


def apply(abaf: ABAF, semantics_specification: str):
    if semantics_specification == 'Stable':
        return get_stable_extensions.apply(abaf)
    if semantics_specification == 'Preferred':
        return get_preferred_extensions.apply(abaf)
    if semantics_specification == 'Conflict-Free':
        return get_conflict_free_extensions.apply(abaf)
    if semantics_specification == 'Naive':
        return get_naive_extensions.apply(abaf)
    if semantics_specification == 'Admissible':
        return get_admissible_extensions.apply(abaf)
    if semantics_specification == 'Complete':
        return get_complete_extensions.apply(abaf)
    if semantics_specification == 'SemiStable':
        return get_semi_stable_extensions.apply(abaf)
    if semantics_specification == 'Ground':
        return get_ground_extensions.apply(abaf)