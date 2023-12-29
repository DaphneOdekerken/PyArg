from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.semantics.get_complete_extensions \
    import get_complete_extensions


# We thank Anh Kiet Nguyen for pointing out that semi-stable assumption
# extensions cannot in general be attained from the instantiated AF.
# cf. Caminada, M., Sá, S., Alcântara, J., & Dvořák, W. (2015). On the
# difference between assumption-based argumentation and abstract argumentation.
# IFCoLog Journal of Logic and its Applications, 2(1), 15-34.
def get_semi_stable_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    complete_extensions = get_complete_extensions(aba_framework)
    extension_and_attacked = {}
    for extension in complete_extensions:
        extension_and_attacked[extension] = set(extension.copy())

        # Add also the arguments that are attacked by this argument.
        for argument in af.arguments:
            if argument.premise <= extension and \
                    argument.conclusion not in aba_framework.assumptions:
                conclusion_index = \
                    list(aba_framework.contraries.values()).index(
                        argument.conclusion)
                extension_and_attacked[extension].add(list(
                    aba_framework.contraries.keys())[conclusion_index])

    ss_ext = set()
    for ext1 in complete_extensions:
        if not any(extension_and_attacked[ext2] > extension_and_attacked[ext1]
                   for ext2 in complete_extensions):
            ss_ext.add(ext1)

    return ss_ext
