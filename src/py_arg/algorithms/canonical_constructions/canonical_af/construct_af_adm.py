
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_af.canonical_def as canonical_def
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
import py_arg.algorithms.canonical_constructions.check_conf_sens as check_conf_sens


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if check_conf_sens.apply(extension_set) and frozenset() in extension_set:
        return canonical_def.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])


