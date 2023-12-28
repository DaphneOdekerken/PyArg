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
# Adjustment based on Definition 3 from Modgil, Sanjay and Martin Caminada.
# "Proof Theories and Algorithms for Abstract Argumentation Frameworks." In
# Argumentation in Artificial Intelligence (2009): 105–132

T = TypeVar('T', bound=Argument)


def _update_complete_extensions_by_labelling(
        argumentation_framework: AbstractArgumentationFramework,
        extensions: Set[FrozenSet[T]],
        labelling: Dict[T, ExtendedExtensionLabel]):
    # Collect UNDEC arguments from labelling.
    candidate_complete_undec = \
        {argument for argument in argumentation_framework.arguments
         if labelling[argument] == ExtendedExtensionLabel.UNDEC}

    # Check if they are allowed to be labelled UNDEC by complete semantics.
    for argument in candidate_complete_undec:
        defeaters = \
            argumentation_framework.get_incoming_defeat_arguments(argument)
        if any(labelling[defeater] == ExtendedExtensionLabel.IN
               for defeater in defeaters):
            # This argument should not be labelled UNDEC (but OUT), so this
            # labelling does not correspond to a complete extension.
            return
        if all(labelling[defeater] == ExtendedExtensionLabel.OUT
               for defeater in defeaters):
            # This argument should not be labelled UNDEC (but IN), so this
            # labelling does not correspond to a complete extension.
            return

    # If we have not returned at this point, we found a complete extension.
    # Collect IN arguments from labelling.
    complete_extension = frozenset(sorted(
        {argument for argument in argumentation_framework.arguments
         if labelling[argument] == ExtendedExtensionLabel.IN}))
    extensions.add(complete_extension)


def get_complete_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    """
    Get the complete extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
    need the complete extensions.
    :return: complete extensions of the argumentation framework.
    """
    initial_labelling = {argument: ExtendedExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return recursively_get_extensions(
        argumentation_framework, initial_labelling, set(),
        _update_complete_extensions_by_labelling)
