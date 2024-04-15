from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.semantics.\
    get_conflict_free_extensions import get_conflict_free_extensions


def get_naive_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    conflict_free_extensions = get_conflict_free_extensions(aba_framework)
    minimal_conflict_free = {
        extension for extension in conflict_free_extensions
        if not any(other_extension < extension
                   for other_extension in conflict_free_extensions)
    }
    return minimal_conflict_free
