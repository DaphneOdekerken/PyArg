from typing import Set

from src import py_arg as canonical_com, py_arg as check_set_com_closed, py_arg as check_intersection_in
import src.py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty

from src.py_arg.aba_classes.aba_framework import ABAF


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_set_com_closed.apply(extension_set) and check_intersection_in.apply(extension_set) and \
            check_non_empty.apply(extension_set):
        return canonical_com.apply(extension_set)
    return ABAF(set(), set(), set(), {})
