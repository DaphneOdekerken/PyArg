
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_cf as canonical_cf
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
import py_arg.algorithms.canonical_constructions.aux_operators as aux_operators
import py_arg.algorithms.canonical_constructions.check_dcl_tight as check_dcl_tight
import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if check_incomparable.apply(extension_set) and check_dcl_tight.apply(aux_operators.dcl(extension_set)) \
            and check_non_empty.apply(extension_set):
        return canonical_cf.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
