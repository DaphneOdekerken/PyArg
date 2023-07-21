
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
import py_arg.algorithms.canonical_constructions.check_downward_closed as check_downward_closed
from py_arg.algorithms.canonical_constructions import check_tight


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if check_downward_closed.apply(extension_set) and check_tight.apply(extension_set):
        return canonical_cf.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
