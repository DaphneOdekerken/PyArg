from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_extensions_recursive import \
    recursively_get_extensions
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    ExtendedExtensionLabel


# Adapted from Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E.
# Dunne. "Algorithms for decision problems in argument systems
# under preferred semantics." Artificial Intelligence 207 (2014): 23-51.
# Adjustment based on Modgil, Sanjay and Martin Caminada. "Proof Theories and
# Algorithms for Abstract Argumentation
# Frameworks." In Iyad Rahwan and Guillermo R. Simari, editors, Argumentation
# in Artificial Intelligence, pages 105–132


def _update_stable_extensions_by_labelling(
        argumentation_framework: AbstractArgumentationFramework,
        extensions: Set[FrozenSet[Argument]],
        labelling: Dict[Argument, ExtendedExtensionLabel]):
    # Collect the IN arguments for those labellings where nothing is UNDEC.
    if all(labelling[argument] != ExtendedExtensionLabel.UNDEC
           for argument in argumentation_framework.arguments):
        extensions.add(frozenset(sorted({
            argument for argument in argumentation_framework.arguments
            if labelling[argument] == ExtendedExtensionLabel.IN})))


def get_stable_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[Argument]]:
    """
    Get the stable extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
    need the stable extensions.
    :return: stable extension of the argumentation framework.
    """
    initial_labelling = {argument: ExtendedExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return recursively_get_extensions(
        argumentation_framework, initial_labelling, set(),
        _update_stable_extensions_by_labelling)
