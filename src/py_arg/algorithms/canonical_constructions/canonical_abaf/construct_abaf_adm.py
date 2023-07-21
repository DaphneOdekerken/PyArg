
from typing import Set

import py_arg.algorithms.canonical_constructions.check_set_conf_sens as check_set_conf_sens
import py_arg.algorithms.canonical_constructions.check_contains_empty as check_contains_empty
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.algorithms.canonical_constructions.canonical_abaf import canonical_adm


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_set_conf_sens.apply(extension_set) and check_contains_empty.apply(extension_set):
        return canonical_adm.apply(extension_set)
    return ABAF(set(), set(), set(), {})
