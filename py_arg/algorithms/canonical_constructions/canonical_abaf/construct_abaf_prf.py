
from typing import Set

import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_st as canonical_st
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
import py_arg.algorithms.canonical_constructions.check_tight as check_tight
import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
import py_arg.algorithms.canonical_constructions.check_non_empty as check_non_empty
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.atom import Atom
from py_arg.aba_classes.rule import Rule
from py_arg.aba_classes.instantiated_argument import InstantiatedArgument


@staticmethod
def apply(extension_set: Set) -> ABAF:
    if check_incomparable.apply(extension_set) and check_non_empty.apply(extension_set):
        return canonical_st.apply(extension_set)
    return ABAF(set(), set(), set(), {})
