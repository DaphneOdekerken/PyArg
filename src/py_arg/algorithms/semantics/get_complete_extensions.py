from enum import Enum
from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.


class CompleteExtensionLabel(Enum):
    IN = 1  # Arguments *might* be in a complete extension
    OUT = 2  # Argument is defeated by an IN argument
    BLANK = 3  # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4  # Argument defeats IN argument
    UNDEC = 5  # Argument may not be included in a complete extension because not defended by any IN argument.


def get_complete_extensions(argumentation_framework: AbstractArgumentationFramework) -> Set[FrozenSet[Argument]]:
    """
    Get the complete extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the complete extensions.
    :return: complete extensions of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> ces = get_complete_extensions(af)
    >>> len(ces)
    1
    >>> frozenset({b, d}) in ces
    True
    >>> frozenset({b}) in ces
    False
    """
    initial_labelling = {argument: CompleteExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return _recursively_get_complete_extensions(argumentation_framework, initial_labelling, set())


def _recursively_get_complete_extensions(argumentation_framework: AbstractArgumentationFramework,
                                         labelling: Dict[Argument, CompleteExtensionLabel],
                                         complete_extensions: Set[FrozenSet[Argument]]) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != CompleteExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != CompleteExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_complete_extension = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                             if labelling[argument] == CompleteExtensionLabel.IN}))

            candidate_complete_undec = {argument for argument in argumentation_framework.arguments
                                        if labelling[argument] == CompleteExtensionLabel.UNDEC}
            legally_undec = set()
            for argument in candidate_complete_undec:
                if all(labelling[defeater] != CompleteExtensionLabel.IN for defeater in
                       argumentation_framework.get_incoming_defeat_arguments(argument)) and \
                        not all(labelling[defeater_out] == CompleteExtensionLabel.OUT for defeater_out in
                                argumentation_framework.get_incoming_defeat_arguments(argument)):
                    legally_undec.add(argument)
            if legally_undec == candidate_complete_undec:
                complete_extensions.add(candidate_complete_extension)
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == CompleteExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        complete_extensions = _recursively_get_complete_extensions(argumentation_framework, alternative_labelling,
                                                                   complete_extensions)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        complete_extensions = _recursively_get_complete_extensions(argumentation_framework, alternative_labelling,
                                                                   complete_extensions)
    return complete_extensions


def _in_trans(labelling: Dict[Argument, CompleteExtensionLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, CompleteExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = CompleteExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = CompleteExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != CompleteExtensionLabel.OUT:
            new_labelling[defeated] = CompleteExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, CompleteExtensionLabel], argument: Argument) -> \
        Dict[Argument, CompleteExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = CompleteExtensionLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
