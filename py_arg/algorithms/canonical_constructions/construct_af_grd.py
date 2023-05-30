
from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux_operators
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if len(extension_set) == 1:
        return AbstractArgumentationFramework('', arguments=list(aux_operators.big_a(extension_set)), defeats=[])
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
