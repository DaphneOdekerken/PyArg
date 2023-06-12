
from typing import Set

from src import py_arg as canonical_cf, py_arg as check_incomparable, py_arg as aux
import src.py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty
from src.py_arg.aba_classes.aba_framework import ABAF


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_non_empty.apply(extension_set) and check_incomparable.apply(extension_set):
        return canonical_cf.apply(aux.dcl(extension_set))
    return ABAF(set(), set(), set(), {})
