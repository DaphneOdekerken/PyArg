
from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.\
    check_set_conf_sens as check_set_conf_sens
import py_arg.abstract_argumentation.canonical_constructions.\
    check_contains_empty as check_contains_empty
from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.canonical_constructions import \
    canonical_adm


@staticmethod
def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if check_set_conf_sens.apply(extension_set) and \
            check_contains_empty.apply(extension_set):
        return canonical_adm.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
