from typing import Set

import py_arg.abstract_argumentation.semantics.get_stable_extensions as \
    get_stable_extensions
from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf import get_canonical_cf_framework
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat


def get_canonical_st_framework(extension_set: Set) -> \
        AbstractArgumentationFramework:
    """
    This implements Definition 12 of Dunne et al., 2015.
    """
    canonical_cf_af = get_canonical_cf_framework(extension_set)
    stable_extensions = get_stable_extensions.get_stable_extensions(
        canonical_cf_af)
    set_x = stable_extensions.difference(extension_set)
    arguments = set(canonical_cf_af.arguments)
    defeats = set(canonical_cf_af.defeats)
    for extension_in_x in set_x:
        # Create a new, self-attacking argument.
        new_argument = Argument(str(set(extension_in_x)))
        arguments.add(new_argument)
        defeats.add(Defeat(new_argument, new_argument))
        # This new argument must be defeated by every argument not in
        # extension_in_x.
        extra_defeating_arguments = \
            set(canonical_cf_af.arguments).difference(extension_in_x)
        for argument_in_extension_in_x in extra_defeating_arguments:
            defeats.add(Defeat(argument_in_extension_in_x, new_argument))

    return AbstractArgumentationFramework(
        '', arguments=list(arguments), defeats=list(defeats))
