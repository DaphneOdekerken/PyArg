from enum import Enum
from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.


class AdmissibleLabel(Enum):
    IN = 1  # Arguments *might* be in an admissible set
    OUT = 2  # Argument is defeated by an IN argument
    BLANK = 3  # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4  # Argument defeats IN argument
    UNDEC = 5  # Argument may not be included in an admissible set because not defended by any IN argument.


def get_admissible_sets(argumentation_framework: AbstractArgumentationFramework) -> Set[FrozenSet[Argument]]:
    """
    Get the admissible sets of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the admissible sets.
    :return: admissible sets of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> ads = get_admissible_sets(af)
    >>> len(ads)
    4
    >>> frozenset({b, d}) in ads
    True
    >>> frozenset({c}) in ads
    False
    """
    initial_labelling = {argument: AdmissibleLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return _recursively_get_admissible_sets(argumentation_framework, initial_labelling, set())


def _recursively_get_admissible_sets(argumentation_framework: AbstractArgumentationFramework,
                                     labelling: Dict[Argument, AdmissibleLabel],
                                     admissible_sets: Set[FrozenSet[Argument]]) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != AdmissibleLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != AdmissibleLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_admissible_set = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                         if labelling[argument] == AdmissibleLabel.IN}))
            admissible_sets.add(candidate_admissible_set)
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == AdmissibleLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        admissible_sets = _recursively_get_admissible_sets(argumentation_framework, alternative_labelling,
                                                           admissible_sets)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        admissible_sets = _recursively_get_admissible_sets(argumentation_framework, alternative_labelling,
                                                           admissible_sets)
    return admissible_sets


def _in_trans(labelling: Dict[Argument, AdmissibleLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, AdmissibleLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = AdmissibleLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = AdmissibleLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != AdmissibleLabel.OUT:
            new_labelling[defeated] = AdmissibleLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, AdmissibleLabel], argument: Argument) -> \
        Dict[Argument, AdmissibleLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = AdmissibleLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
