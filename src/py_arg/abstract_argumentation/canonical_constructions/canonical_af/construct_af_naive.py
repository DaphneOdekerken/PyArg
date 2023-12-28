from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .canonical_cf as canonical_cf
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_dcl_tight, is_non_empty
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.canonical_constructions import aux_operators


def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if is_incomparable(extension_set) and \
            is_dcl_tight(aux_operators.dcl(extension_set)) and \
            is_non_empty(extension_set):
        return canonical_cf.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
