from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.aba_classes.semantics.get_complete_extensions as get_complete_extensions


# We thank Anh Kiet Nguyen for pointing out that semi-stable assumption extensions
# cannot in general be attained from the instantiated af.
# cf. 'ON THE DIFFERENCE BETWEEN ASSUMPTION-BASED ARGUMENTATION AND ABSTRACT ARGUMENTATION'
def get_semi_stable_extensions(aba_framework: ABAF) -> Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    com_ext = get_complete_extensions.get_complete_extensions(aba_framework)
    extension_reach = {}
    for ext in com_ext:
        extension_reach[ext] = set(ext.copy())
        for arg in af.arguments:
            if arg.premise.issubset(ext) and arg.conclusion not in aba_framework.assumptions:
                conclusion_index = list(aba_framework.contraries.values()).index(arg.conclusion)
                extension_reach[ext].add(list(aba_framework.contraries.keys())[conclusion_index])
    ss_ext = set()
    for ext1 in com_ext:
        is_semi_stable = True
        for ext2 in com_ext:
            if extension_reach[ext1].issubset(extension_reach[ext2]) and \
                    not extension_reach[ext2].issubset(extension_reach[ext1]):
                is_semi_stable = False
        if is_semi_stable:
            ss_ext.add(ext1)

    return ss_ext
