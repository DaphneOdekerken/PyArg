from enum import Enum
from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.
# Adjustment based on Modgil, Sanjay and Martin Caminada. "Proof Theories and Algorithms for Abstract Argumentation 
# Frameworks." In Iyad Rahwan and Guillermo R. Simari, editors, Argumentation in Artificial Intelligence, pages 105–132


class SemiStableExtensionLabel(Enum):
    IN = 1  # Arguments *might* be in a semi-stable extension
    OUT = 2  # Argument is defeated by an IN argument
    BLANK = 3  # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4  # Argument defeats IN argument
    UNDEC = 5  # Argument may not be included in a semi-stable extension because not defended by any IN argument.


def get_semistable_extensions(argumentation_framework: AbstractArgumentationFramework) -> Set[FrozenSet[Argument]]:
    """
    Get the semi-stable extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the semi-stable extensions.
    :return: semi-stable extension of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> sses = get_semistable_extensions(af)
    >>> len(sses)
    1
    >>> frozenset({b, d}) in sses
    True
    >>> frozenset({b}) in sses
    False
    """
    initial_labelling = {argument: SemiStableExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return _recursively_get_semistable_extensions(argumentation_framework, initial_labelling, [])


def _recursively_get_semistable_extensions(argumentation_framework: AbstractArgumentationFramework,
                                           labelling: Dict[Argument, SemiStableExtensionLabel],
                                           labellings) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != SemiStableExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != SemiStableExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_semistable_undec = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                           if labelling[argument] == SemiStableExtensionLabel.UNDEC}))
            calculated_semistable_undec = []
            for ss_labelling in labellings:
                calculated_semistable_undec.append(
                    [frozenset(sorted({argument for argument in argumentation_framework.arguments
                                       if ss_labelling[argument] == SemiStableExtensionLabel.UNDEC})),
                     ss_labelling])
            if not any(candidate_semistable_undec > semistable_undec[0]
                       for semistable_undec in calculated_semistable_undec):
                labellings.append(labelling)
                if any(candidate_semistable_undec < semistable_undec[0]
                       for semistable_undec in calculated_semistable_undec):
                    for semistable_undec in calculated_semistable_undec:
                        if candidate_semistable_undec < semistable_undec[0]:
                            labellings.remove(semistable_undec[1])
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == SemiStableExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        semistable_extensions = _recursively_get_semistable_extensions(argumentation_framework, alternative_labelling,
                                                                       labellings)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        semistable_extensions = _recursively_get_semistable_extensions(argumentation_framework, alternative_labelling,
                                                                       labellings)
    semistable_extensions = set()
    for labelling in labellings:
        semistable_extensions.add(frozenset(sorted({argument for argument in argumentation_framework.arguments if
                                                    labelling[argument] == SemiStableExtensionLabel.IN})))

    return semistable_extensions


def _in_trans(labelling: Dict[Argument, SemiStableExtensionLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, SemiStableExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = SemiStableExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = SemiStableExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != SemiStableExtensionLabel.OUT:
            new_labelling[defeated] = SemiStableExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, SemiStableExtensionLabel], argument: Argument) -> \
        Dict[Argument, SemiStableExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = SemiStableExtensionLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
