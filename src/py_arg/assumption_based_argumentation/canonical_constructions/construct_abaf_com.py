from typing import Set

import py_arg.assumption_based_argumentation.canonical_constructions.\
    canonical_com as canonical_com
import py_arg.abstract_argumentation.canonical_constructions.\
    check_set_com_closed as check_set_com_closed
import py_arg.abstract_argumentation.canonical_constructions.\
    check_intersection_in as check_intersection_in
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_non_empty

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if check_set_com_closed.apply(extension_set) and \
            check_intersection_in.apply(extension_set) and \
            is_non_empty(extension_set):
        return canonical_com.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
