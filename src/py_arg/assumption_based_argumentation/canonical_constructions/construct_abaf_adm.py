from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.\
    check_set_conf_sens as check_set_conf_sens
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import contains_empty_set
from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.canonical_constructions import \
    canonical_adm


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    if check_set_conf_sens.apply(extension_set) and \
            contains_empty_set(extension_set):
        return canonical_adm.apply(extension_set)
    return AssumptionBasedArgumentationFramework(set(), set(), set(), {})
