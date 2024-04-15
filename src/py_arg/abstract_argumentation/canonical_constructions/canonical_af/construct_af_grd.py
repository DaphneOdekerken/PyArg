from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
    aux
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def construct_argumentation_framework_grounded(extension_set: Set) -> \
        AbstractArgumentationFramework:
    if len(extension_set) == 1:
        return AbstractArgumentationFramework('', arguments=list(aux.big_a(
            extension_set)), defeats=[])
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
