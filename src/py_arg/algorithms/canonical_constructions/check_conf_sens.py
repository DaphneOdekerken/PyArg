
from typing import Set

import py_arg as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    pairs_ = aux.pairs(extension_set)

    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.union(ext2) not in extension_set:
            boolean = False
            for lit1 in ext1:
                for lit2 in ext2:
                    temp = frozenset({lit1, lit2})
                    if temp not in pairs_:
                        boolean = True
            if not boolean:
                return False
    return True
