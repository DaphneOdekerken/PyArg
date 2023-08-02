
from typing import Set

import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
import py_arg.algorithms.canonical_constructions.aux_operators as aux
import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.algorithms.canonical_constructions.canonical_abaf import canonical_st


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_non_empty.apply(extension_set) and check_incomparable.apply(extension_set):
        return canonical_st.apply(extension_set)
    return ABAF(set(), set(), set(), {})
