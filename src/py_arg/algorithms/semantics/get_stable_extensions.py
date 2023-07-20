from enum import Enum
from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.
# Adjustment based on Modgil, Sanjay and Martin Caminada. "Proof Theories and Algorithms for Abstract Argumentation 
# Frameworks." In Iyad Rahwan and Guillermo R. Simari, editors, Argumentation in Artificial Intelligence, pages 105–132


class StableExtensionLabel(Enum):
    IN = 1  # Arguments *might* be in a stable extension
    OUT = 2  # Argument is defeated by an IN argument
    BLANK = 3  # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4  # Argument defeats IN argument
    UNDEC = 5  # Argument may not be included in a stable extension because not defended by any IN argument.


def get_stable_extensions(argumentation_framework: AbstractArgumentationFramework) -> Set[FrozenSet[Argument]]:
    """
    Get the stable extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the stable extensions.
    :return: stable extension of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> ses = get_stable_extensions(af)
    >>> len(ses)
    1
    >>> frozenset({b, d}) in ses
    True
    >>> frozenset({b}) in ses
    False
    """
    initial_labelling = {argument: StableExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return _recursively_get_stable_extensions(argumentation_framework, initial_labelling, set())


def _recursively_get_stable_extensions(argumentation_framework: AbstractArgumentationFramework,
                                       labelling: Dict[Argument, StableExtensionLabel],
                                       stable_extensions: Set[FrozenSet[Argument]]) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != StableExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != StableExtensionLabel.MUST_OUT and labelling[
            argument] != StableExtensionLabel.UNDEC
               for argument in argumentation_framework.arguments):
            stable_extensions.add(frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                    if labelling[argument] == StableExtensionLabel.IN})))
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == StableExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        stable_extensions = _recursively_get_stable_extensions(argumentation_framework, alternative_labelling,
                                                               stable_extensions)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        stable_extensions = _recursively_get_stable_extensions(argumentation_framework, alternative_labelling,
                                                               stable_extensions)
    return stable_extensions


def _in_trans(labelling: Dict[Argument, StableExtensionLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, StableExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = StableExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = StableExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != StableExtensionLabel.OUT:
            new_labelling[defeated] = StableExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, StableExtensionLabel], argument: Argument) -> \
        Dict[Argument, StableExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = StableExtensionLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
