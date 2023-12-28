from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf as canonical_cf
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_downward_closed, is_tight
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if is_downward_closed(extension_set) and is_tight(extension_set):
        return canonical_cf.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
