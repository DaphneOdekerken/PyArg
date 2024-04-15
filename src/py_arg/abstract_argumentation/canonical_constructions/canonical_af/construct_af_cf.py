from typing import Set

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf import get_canonical_cf_framework
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_downward_closed, is_tight
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def construct_argumentation_framework_conflict_free(extension_set: Set) -> \
        AbstractArgumentationFramework:
    if is_downward_closed(extension_set) and is_tight(extension_set):
        return get_canonical_cf_framework(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
