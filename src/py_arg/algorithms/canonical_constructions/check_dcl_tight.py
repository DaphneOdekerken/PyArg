
from typing import Set

from py_arg.algorithms.canonical_constructions import check_tight
from py_arg.algorithms.canonical_constructions import aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    return check_tight.apply(aux.dcl(extension_set))
