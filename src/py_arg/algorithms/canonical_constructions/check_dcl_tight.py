
from typing import Set

from src import py_arg as aux, py_arg as check_tight


@staticmethod
def apply(extension_set: Set) -> bool:
    return check_tight.apply(aux.dcl(extension_set))
