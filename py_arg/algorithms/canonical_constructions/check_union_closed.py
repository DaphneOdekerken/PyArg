
from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    if frozenset() not in extension_set:
        return False
    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.union(ext2) not in extension_set:
            return False
    return True
