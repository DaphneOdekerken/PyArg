
from typing import Set

import py_arg.algorithms.canonical_constructions.aux_operators as aux
import py_arg.algorithms.canonical_constructions.check_tight as check_tight


@staticmethod
def apply(extension_set: Set) -> bool:
    return check_tight.apply(aux.dcl(extension_set))
