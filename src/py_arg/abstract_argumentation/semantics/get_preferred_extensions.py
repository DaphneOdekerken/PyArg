from typing import Set, Dict, FrozenSet, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.extended_extension_label import \
    ExtendedExtensionLabel
from py_arg.abstract_argumentation.semantics.get_extensions_recursive import \
    recursively_get_extensions


# Algorithm 1 from Samer Nofal, Katie Atkinson and Paul E. Dunne.
# "Algorithms for decision problems in argument systems under preferred
# semantics." Artificial Intelligence 207 (2014): 23-51.

T = TypeVar('T', bound=Argument)


def _update_preferred_extensions_by_labelling(
        argumentation_framework: AbstractArgumentationFramework,
        extensions: Set[FrozenSet[T]],
        labelling: Dict[T, ExtendedExtensionLabel]):
    # Collect the IN arguments.
    candidate_preferred_extension = frozenset(sorted({
        argument for argument in argumentation_framework.arguments
        if labelling[argument] == ExtendedExtensionLabel.IN}))
    # Only keep this extension if no other extension that was found
    # earlier is a proper subset of this one.
    if not any(candidate_preferred_extension < preferred_extension
               for preferred_extension in extensions):
        extensions.add(candidate_preferred_extension)


def get_preferred_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    """
    Get the preferred extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for
        which we need the preferred extensions.
    :return: Preferred extension of the argumentation framework.
    """
    initial_labelling = {argument: ExtendedExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return recursively_get_extensions(
        argumentation_framework, initial_labelling, set(),
        _update_preferred_extensions_by_labelling)
