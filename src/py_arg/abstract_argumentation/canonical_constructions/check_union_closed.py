from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
    aux


def apply(extension_set: Set) -> bool:
    if frozenset() not in extension_set:
        return False
    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.union(ext2) not in extension_set:
            return False
    return True
