
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_af.canonical_st as canonical_st
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
from py_arg.algorithms.canonical_constructions import check_tight


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if check_incomparable.apply(extension_set) and check_tight.apply(extension_set) and len(extension_set) != 0:
        return canonical_st.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])


