from typing import Set

import py_arg.assumption_based_argumentation.canonical_constructions.\
    canonical_st as canonical_st
import py_arg.abstract_argumentation.canonical_constructions.\
    check_incomparable as check_incomparable
from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.classes.rule import Rule


@staticmethod
def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if len(extension_set) == 0:
        return AssumptionBasedArgumentationFramework(
            {'x'}, {Rule('', {'x'}, 'x_c')}, {'x', 'x_c'}, {'x': 'x_c'})
    if check_incomparable.apply(extension_set):
        return canonical_st.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
