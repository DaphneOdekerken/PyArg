
from typing import Set


@staticmethod
def apply(extension_set: Set) -> bool:
    return frozenset({}) in extension_set
