from typing import Set

import py_arg.assumption_based_argumentation.canonical_constructions.\
    canonical_st as canonical_st
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_non_empty
from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if is_incomparable(extension_set) and is_non_empty(
            extension_set):
        return canonical_st.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
