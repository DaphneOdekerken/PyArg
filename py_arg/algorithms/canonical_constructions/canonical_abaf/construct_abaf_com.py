from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_com as canonical_com
import py_arg.algorithms.canonical_constructions.check_set_com_closed as check_set_com_closed
import py_arg.algorithms.canonical_constructions.check_intersection_in as check_intersection_in
import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty

from py_arg.aba_classes.aba_framework import ABAF


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_set_com_closed.apply(extension_set) and check_intersection_in.apply(extension_set) and \
            check_non_empty.apply(extension_set):
        return canonical_com.apply(extension_set)
    return ABAF(set(), set(), set(), {})
