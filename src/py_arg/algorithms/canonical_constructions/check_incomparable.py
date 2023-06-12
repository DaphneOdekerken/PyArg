
from typing import Set

from src import py_arg as aux


@staticmethod
def apply(extension_set: Set) -> bool:
    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.intersection(ext2) == ext1:
            return False
        if ext1.intersection(ext2) == ext2:
            return False
    return True
