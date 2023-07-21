
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_st as canonical_st
import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
from py_arg.aba_classes.aba_framework import ABAF


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_incomparable.apply(extension_set):
        return canonical_st.apply(extension_set)
    return ABAF(set(), set(), set(), {})
