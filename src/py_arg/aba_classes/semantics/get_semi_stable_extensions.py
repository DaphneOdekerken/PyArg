from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.aba_classes.semantics.get_complete_extensions as get_complete_extensions


# We thank Anh Kiet Nguyen for reminding us that semi-stable assumption extensions
# cannot in general be attained from the instantiated af.
# cf. 'ON THE DIFFERENCE BETWEEN ASSUMPTION-BASED ARGUMENTATION AND ABSTRACT ARGUMENTATION'
def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    af = abaf.generate_af()
    com_ext = get_complete_extensions.apply(abaf)
    extension_reach = {}
    for ext in com_ext:
        extension_reach[ext] = set(ext.copy())
        for arg in af.arguments:
            if arg.premise.issubset(ext):
                if arg.conclusion not in abaf.assumptions:
                    extension_reach[ext].add(
                        list(abaf.contraries.keys())[list(abaf.contraries.values()).index(arg.conclusion)])
    ss_ext = set()
    for ext1 in com_ext:
        is_semistable = True
        for ext2 in com_ext:
            if extension_reach[ext1].issubset(extension_reach[ext2]) and \
                    not extension_reach[ext2].issubset(extension_reach[ext1]):
                is_semistable = False
        if is_semistable:
            ss_ext.add(ext1)

    return ss_ext
