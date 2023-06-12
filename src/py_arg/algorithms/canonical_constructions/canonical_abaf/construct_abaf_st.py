
from typing import Set

import src.py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_st as canonical_st
from src import py_arg as check_incomparable
from src.py_arg.aba_classes.aba_framework import ABAF


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_incomparable.apply(extension_set):
        return canonical_st.apply(extension_set)
    return ABAF(set(), set(), set(), {})
