from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
   aux


def apply(extension_set: Set) -> bool:
    p = aux.big_p(extension_set)

    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.union(ext2) not in extension_set:
            boolean = False
            diff1 = ext1.difference(ext2)
            diff2 = ext2.difference(ext1)
            for el in diff1:
                if ext2.union({el}) in p:
                    boolean = True
                    continue
            for el in diff2:
                if ext1.union({el}) in p:
                    boolean = True
                    continue
            if not boolean:
                return False
    return True
