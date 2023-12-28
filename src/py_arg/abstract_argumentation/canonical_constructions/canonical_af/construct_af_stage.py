from typing import Set

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_st import get_canonical_st_framework
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_tight
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def construct_argumentation_framework_stage(extension_set: Set) -> \
        AbstractArgumentationFramework:
    if is_incomparable(extension_set) and is_tight(
            extension_set) and len(extension_set) != 0:
        return get_canonical_st_framework(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
