
from typing import Set

import src.py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf
from src.py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from src import py_arg as aux_operators, py_arg as check_dcl_tight, py_arg as check_incomparable
import src.py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if check_incomparable.apply(extension_set) and check_dcl_tight.apply(aux_operators.dcl(extension_set)) \
            and check_non_empty.apply(extension_set):
        return canonical_cf.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
