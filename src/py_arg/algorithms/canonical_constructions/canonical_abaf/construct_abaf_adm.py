
from typing import Set

from src import py_arg as canonical_adm, py_arg as check_set_conf_sens
import src.py_arg.algorithms.canonical_constructions.check_contains_empty as check_contains_empty
from src.py_arg.aba_classes.aba_framework import ABAF


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_set_conf_sens.apply(extension_set) and check_contains_empty.apply(extension_set):
        return canonical_adm.apply(extension_set)
    return ABAF(set(), set(), set(), {})
