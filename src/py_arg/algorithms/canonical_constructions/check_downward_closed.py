
from typing import Set

from src import py_arg as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    return aux.dcl(extension_set).__eq__(extension_set)
