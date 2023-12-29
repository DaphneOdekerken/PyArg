from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
import py_arg.assumption_based_argumentation.semantics.get_stable_extensions \
    as get_stable_extensions
import py_arg.assumption_based_argumentation.\
    semantics.get_complete_extensions as get_complete_extensions
import py_arg.assumption_based_argumentation.semantics.\
    get_conflict_free_extensions as get_conflict_free_extensions
import py_arg.assumption_based_argumentation.semantics.\
    get_admissible_extensions as get_admissible_extensions
import py_arg.assumption_based_argumentation.semantics.\
    get_preferred_extensions as get_preferred_extensions
import py_arg.assumption_based_argumentation.semantics.\
    get_semi_stable_extensions as get_semi_stable_extensions
import py_arg.assumption_based_argumentation.semantics.\
    get_grounded_extensions as get_ground_extensions
import py_arg.assumption_based_argumentation.semantics.\
    get_naive_extensions as get_naive_extensions


def apply(abaf: AssumptionBasedArgumentationFramework,
          semantics_specification: str):
    if semantics_specification == 'Stable':
        return get_stable_extensions.get_stable_extensions(abaf)
    if semantics_specification == 'Preferred':
        return get_preferred_extensions.get_preferred_extensions(abaf)
    if semantics_specification == 'Conflict-Free':
        return get_conflict_free_extensions.get_conflict_free_extensions(abaf)
    if semantics_specification == 'Naive':
        return get_naive_extensions.get_naive_extensions(abaf)
    if semantics_specification == 'Admissible':
        return get_admissible_extensions.get_admissible_extensions(abaf)
    if semantics_specification == 'Complete':
        return get_complete_extensions.get_complete_extensions(abaf)
    if semantics_specification == 'SemiStable':
        return get_semi_stable_extensions.get_semi_stable_extensions(abaf)
    if semantics_specification == 'Grounded':
        return get_ground_extensions.get_grounded_extensions(abaf)
