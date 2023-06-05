
from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    power = aux.powerset(extension_set)
    d = aux.dcl(extension_set)
    p = aux.big_p(extension_set)
    for es1, es2 in aux.tuples(power):
        a_es1 = aux.big_a(es1)
        a_es2 = aux.big_a(es2)
        if a_es1 in d:
            if a_es2 in d:
                c = aux.big_c(a_es1.union(a_es2), extension_set)
                if len(c) != 1:
                    boolean = False
                    for lit in a_es2:
                        temp = set(a_es1.copy())
                        temp.add(lit)
                        temp = frozenset(temp)
                        if temp in p:
                            boolean = True
                    if not boolean:
                        return False

                    for lit in a_es1:
                        temp = set(a_es2.copy())
                        temp.add(lit)
                        temp = frozenset(temp)
                        if temp in p:
                            boolean = True

                    if not boolean:
                        return False
    return True
