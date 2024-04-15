from typing import Set

from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_non_empty, is_downward_closed
from py_arg.assumption_based_argumentation.canonical_constructions import \
    canonical_cf
from py_arg.assumption_based_argumentation.classes.aba_framework \
    import AssumptionBasedArgumentationFramework


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if is_non_empty(extension_set) and is_downward_closed(extension_set):
        return canonical_cf.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
