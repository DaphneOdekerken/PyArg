from enum import Enum
from typing import Set, Dict, FrozenSet, List, Any

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.


class IdealExtensionLabel(Enum):
    IN = 1  # Arguments *might* be in a preferred extension
    OUT = 2  # Argument is defeated by an IN argument
    BLANK = 3  # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4  # Argument defeats IN argument
    UNDEC = 5  # Argument may not be included in a preferred extension because not defended by any IN argument.


def get_ideal_extension(argumentation_framework: AbstractArgumentationFramework) -> List[Set[Any]]:
    """
    Get the ideal extension of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the ideal extension.
    :return: ideal extension of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> idl = get_ideal_extension(af)
    >>> len(idl)
    1
    >>> frozenset({b, d}) in idl
    True
    >>> frozenset({b}) in idl
    False
    """
    initial_labelling = {argument: IdealExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    frozen_admissible_sets = _recursively_get_admissible_sets(argumentation_framework, initial_labelling, set())
    admissible_sets = [set(frozen_admissible_set) for frozen_admissible_set in frozen_admissible_sets]
    preferred_extensions = []
    for candidate_preferred_extension in admissible_sets:
        if not any(candidate_preferred_extension < admissible_set
                   for admissible_set in admissible_sets):
            preferred_extensions.append(candidate_preferred_extension)
    intersect_preferred = set.intersection(*preferred_extensions)
    admissible_subsets = [admissible_set for admissible_set in admissible_sets if
                          intersect_preferred.issuperset(admissible_set) == True]
    max_admissible_subsets = []
    for candidate_ideal_extension in admissible_subsets:
        if not any(candidate_ideal_extension < admissible_set
                   for admissible_set in admissible_subsets):
            max_admissible_subsets.append(candidate_ideal_extension)
    return max_admissible_subsets


def _recursively_get_admissible_sets(argumentation_framework: AbstractArgumentationFramework,
                                     labelling: Dict[Argument, IdealExtensionLabel],
                                     admissible_sets: Set[FrozenSet[Argument]]) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != IdealExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != IdealExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_admissible_set = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                         if labelling[argument] == IdealExtensionLabel.IN}))
            admissible_sets.add(candidate_admissible_set)
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == IdealExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        admissible_sets = _recursively_get_admissible_sets(argumentation_framework, alternative_labelling,
                                                           admissible_sets)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        admissible_sets = _recursively_get_admissible_sets(argumentation_framework, alternative_labelling,
                                                           admissible_sets)

    return admissible_sets


def _in_trans(labelling: Dict[Argument, IdealExtensionLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, IdealExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = IdealExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = IdealExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != IdealExtensionLabel.OUT:
            new_labelling[defeated] = IdealExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, IdealExtensionLabel], argument: Argument) -> \
        Dict[Argument, IdealExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = IdealExtensionLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
