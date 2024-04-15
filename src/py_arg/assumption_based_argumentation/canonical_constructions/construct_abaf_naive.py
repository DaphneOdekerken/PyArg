from typing import Set

from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_non_empty, is_incomparable
from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.canonical_constructions import \
    canonical_st


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if is_non_empty(extension_set) and is_incomparable(extension_set):
        return canonical_st.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
