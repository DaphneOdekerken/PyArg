
from typing import Set

from py_arg.algorithms.canonical_constructions import check_downward_closed
from py_arg.algorithms.canonical_constructions.canonical_abaf import canonical_cf

import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty
from py_arg.aba_classes.aba_framework import ABAF



@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_non_empty.apply(extension_set) and check_downward_closed.apply(extension_set):
        return canonical_cf.apply(extension_set)
    return ABAF(set(), set(), set(), {})
