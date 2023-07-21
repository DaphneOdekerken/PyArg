
from typing import Set
from py_arg.algorithms.canonical_constructions import aux_operators as aux

@staticmethod
def apply(extension_set: Set) -> bool:
    a = aux.big_a(extension_set)
    pairs_ = aux.pairs(extension_set)

    for ext in extension_set:
        for lit in a:
            if lit not in ext:
                temp = set(ext.copy())
                temp.add(lit)
                temp = frozenset(temp)
                if temp not in extension_set:
                    boolean = False
                    for lin_in in ext:
                        test = frozenset({lit, lin_in})
                        if test not in pairs_:
                            boolean = True
                    if not boolean:
                        return False
    return True
