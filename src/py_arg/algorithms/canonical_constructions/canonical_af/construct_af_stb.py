
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_af.canonical_st as canonical_st
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.canonical_constructions import check_tight


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if not check_non_empty.apply(extension_set):
        x = Argument('x')
        return AbstractArgumentationFramework('', arguments=[x], defeats=[Defeat(x, x)])
    if check_incomparable.apply(extension_set) and check_tight.apply(extension_set):
        return canonical_st.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
