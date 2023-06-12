
from typing import Set

import src.py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf
from src.py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from src import py_arg as check_tight, py_arg as check_downward_closed


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if check_downward_closed.apply(extension_set) and check_tight.apply(extension_set):
        return canonical_cf.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
