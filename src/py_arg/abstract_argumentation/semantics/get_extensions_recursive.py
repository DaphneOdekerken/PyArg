from typing import Set, Dict, FrozenSet, Callable, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.extended_extension_label import \
    ExtendedExtensionLabel


# This is an abstraction from Algorithm 1 from Samer Nofal, Katie Atkinson and
# Paul E. Dunne. "Algorithms for decision problems in argument systems under
# preferred semantics." Artificial Intelligence 207 (2014): 23-51.

T = TypeVar('T', bound=Argument)


def recursively_get_extensions(
        argumentation_framework: AbstractArgumentationFramework,
        labelling: Dict[T, ExtendedExtensionLabel],
        extensions: Set[FrozenSet[T]],
        update_extensions_by_labelling: Callable[[
            AbstractArgumentationFramework, Set[FrozenSet[T]],
            Dict[T, ExtendedExtensionLabel]], None]) -> \
        Set[FrozenSet[T]]:
    if all(labelling[argument] != ExtendedExtensionLabel.BLANK
           for argument in argumentation_framework.arguments):
        if all(labelling[argument] != ExtendedExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            # All arguments have some label in {IN, OUT, UNDEC}.
            update_extensions_by_labelling(
                argumentation_framework, extensions, labelling)
    else:
        # There must be some BLANK argument(s). Select the first one.
        blank_argument = \
            [argument for argument in argumentation_framework.arguments
             if labelling[argument] == ExtendedExtensionLabel.BLANK][0]

        # Assume that it is IN and get all preferred extensions assuming this.
        alternative_labelling = _in_trans(labelling, blank_argument,
                                          argumentation_framework)
        extensions = recursively_get_extensions(
            argumentation_framework, alternative_labelling,
            extensions, update_extensions_by_labelling)

        # Assume that it might not be part of any preferred extension and
        # get all preferred extensions assuming this.
        alternative_labelling = _undec_trans(labelling, blank_argument)
        extensions = recursively_get_extensions(
            argumentation_framework, alternative_labelling,
            extensions, update_extensions_by_labelling)

    return extensions


def _in_trans(labelling: Dict[T, ExtendedExtensionLabel],
              argument: T,
              argumentation_framework: AbstractArgumentationFramework) -> \
        Dict[T, ExtendedExtensionLabel]:
    # Assume that the argument is IN.
    new_labelling = labelling.copy()
    new_labelling[argument] = ExtendedExtensionLabel.IN

    # Try to make the arguments defeated by the new IN argument OUT.
    for defeated in argumentation_framework.get_outgoing_defeat_arguments(
            argument):
        if defeated == argument:
            break
        else:
            new_labelling[defeated] = ExtendedExtensionLabel.OUT

    # Label the arguments that defeat the new IN argument by MUST_OUT.
    for defeater in argumentation_framework.get_incoming_defeat_arguments(
            argument):
        if new_labelling[defeater] != ExtendedExtensionLabel.OUT:
            new_labelling[defeater] = ExtendedExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[T, ExtendedExtensionLabel],
                 argument: T) -> \
        Dict[Argument, ExtendedExtensionLabel]:
    # Assume that the argument is UNDEC.
    new_labelling = labelling.copy()
    new_labelling[argument] = ExtendedExtensionLabel.UNDEC
    return new_labelling
