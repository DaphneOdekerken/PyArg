from typing import Set
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
import py_arg.algorithms.semantics.get_conflict_free_extensions as get_conflict_free_extensions


def apply(argumentation_framework: AbstractArgumentationFramework) -> Set[frozenset[Argument]]:
    cf_ext = get_conflict_free_extensions.apply(argumentation_framework)
    rm = set()
    for ext1 in cf_ext:
        for ext2 in cf_ext:
            if ext1.issubset(ext2) and not ext2.issubset(ext1):
                rm.add(ext1)
    return cf_ext.difference(rm)

