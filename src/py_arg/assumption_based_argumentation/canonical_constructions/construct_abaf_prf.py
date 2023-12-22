
from typing import Set

import py_arg.assumption_based_argumentation.canonical_constructions.canonical_st as canonical_st
import py_arg.abstract_argumentation.canonical_constructions.check_incomparable as check_incomparable
import py_arg.abstract_argumentation.canonical_constructions.check_non_empty as check_non_empty
from py_arg.assumption_based_argumentation.classes.aba_framework import AssumptionBasedArgumentationFramework


@staticmethod
def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if check_incomparable.apply(extension_set) and check_non_empty.apply(extension_set):
        return canonical_st.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
