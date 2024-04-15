from typing import Set

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf import get_canonical_cf_framework
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_dcl_tight, is_non_empty
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.canonical_constructions import aux_operators


def construct_argumentation_framework_naive(extension_set: Set) -> \
        AbstractArgumentationFramework:
    if is_incomparable(extension_set) and \
            is_dcl_tight(aux_operators.downward_closure(extension_set)) and \
            is_non_empty(extension_set):
        return get_canonical_cf_framework(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
