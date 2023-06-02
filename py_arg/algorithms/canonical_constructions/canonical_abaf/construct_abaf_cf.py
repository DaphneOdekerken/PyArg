
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_cf as canonical_cf
import py_arg.algorithms.canonical_constructions.check_downward_closed as check_downward_closed
import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty
from py_arg.aba_classes.aba_framework import ABAF



@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_non_empty.apply(extension_set) and check_downward_closed.apply(extension_set):
        return canonical_cf.apply(extension_set)
    return ABAF(set(), set(), set(), {})
