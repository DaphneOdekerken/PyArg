
from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    intersection = aux.big_a(extension_set)
    for ext in extension_set:
        intersection = intersection.intersection(ext)
    return intersection in extension_set
