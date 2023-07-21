from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    power = aux.powerset(extension_set)
    pairs_ = aux.pairs(extension_set)

    for es_sub in power:
        a_es_sub = aux.big_a(set(es_sub))
        if len(a_es_sub) == 0:
            continue
        boolean = False

        for lit1, lit2 in aux.tuples(a_es_sub):
            if frozenset({lit1, lit2}) not in pairs_:
                boolean = True
        if not boolean and len(aux.big_c(a_es_sub, extension_set)) != 1:
            return False

    return True
