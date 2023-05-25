
from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    return aux.dcl(extension_set).__eq__(extension_set)
