
from typing import Set

import src.py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf
from src import py_arg as get_stable_extensions
from src.py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from src.py_arg.abstract_argumentation_classes.argument import Argument
from src.py_arg.abstract_argumentation_classes.defeat import Defeat


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    canon_cf = canonical_cf.apply(extension_set)
    canon_cf_stb_ext = get_stable_extensions.get_stable_extensions(canon_cf)
    to_elim = canon_cf_stb_ext.difference(extension_set)
    arguments = set(canon_cf.arguments)
    defeats = set(canon_cf.defeats)
    for el in to_elim:
        new_arg = Argument(str(set(el)))
        arguments.add(new_arg)
        defeats.add(Defeat(new_arg, new_arg))
        for arg in set(canon_cf.arguments).difference(el):
            defeats.add(Defeat(arg, new_arg))

    return AbstractArgumentationFramework('', arguments=list(arguments), defeats=list(defeats))
