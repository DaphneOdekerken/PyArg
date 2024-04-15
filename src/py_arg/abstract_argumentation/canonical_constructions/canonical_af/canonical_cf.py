from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
    aux
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.defeat import Defeat


def get_canonical_cf_framework(extension_set: Set) -> \
        AbstractArgumentationFramework:
    """
    This implements Definition 11 of Dunne et al., 2015.
    """
    all_arguments = list(aux.big_a(extension_set))
    extension_pairs = aux.pairs(extension_set)
    defeats = []
    for element_1, element_2 in aux.tuples(all_arguments):
        if frozenset({element_1, element_2}) not in extension_pairs:
            defeats.append(Defeat(element_1, element_2))
            defeats.append(Defeat(element_2, element_1))

    return AbstractArgumentationFramework(
        '', arguments=all_arguments, defeats=defeats)
