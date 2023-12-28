from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
    aux
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.defeat import Defeat


def apply(extension_set: Set) -> AbstractArgumentationFramework:
    args = aux.big_a(extension_set)
    args = list(args)
    defeats = []
    pairs_ = aux.pairs(extension_set)
    for arg1, arg2 in aux.tuples(args):
        if frozenset({arg1, arg2}) not in pairs_:
            defeats.append(Defeat(arg1, arg2))
            defeats.append(Defeat(arg2, arg1))

    return AbstractArgumentationFramework('', arguments=args, defeats=defeats)
