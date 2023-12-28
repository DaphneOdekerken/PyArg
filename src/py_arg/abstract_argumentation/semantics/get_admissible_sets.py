from typing import Set, Dict, FrozenSet, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_extensions_recursive import \
    recursively_get_extensions
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    ExtendedExtensionLabel


# Adapted from Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E.
# Dunne. "Algorithms for decision problems in argument systems under
# preferred semantics." Artificial Intelligence 207 (2014): 23-51.

T = TypeVar('T', bound=Argument)


def _update_admissible_sets_by_labelling(
        argumentation_framework: AbstractArgumentationFramework,
        extensions: Set[FrozenSet[T]],
        labelling: Dict[T, ExtendedExtensionLabel]):
    # Collect the IN arguments.
    admissible_set = frozenset(sorted({
        argument for argument in argumentation_framework.arguments
        if labelling[argument] == ExtendedExtensionLabel.IN}))
    extensions.add(admissible_set)


def get_admissible_sets(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    """
    Get the admissible sets of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
        need the admissible sets.
    :return: admissible sets of the argumentation framework.
    """
    initial_labelling = {argument: ExtendedExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return recursively_get_extensions(
        argumentation_framework, initial_labelling, set(),
        _update_admissible_sets_by_labelling)
