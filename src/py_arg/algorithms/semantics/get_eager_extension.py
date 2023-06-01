#from _typeshed import SupportsLessThan
from enum import Enum
from typing import Set, Dict, FrozenSet, List, Union, Any

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.
# Adjustment based on Modgil, Sanjay and Martin Caminada. "Proof Theories and Algorithms for Abstract Argumentation 
# Frameworks." In Iyad Rahwan and Guillermo R. Simari, editors, Argumentation in Artificial Intelligence, pages 105–132


class EagerExtensionLabel(Enum):
    IN = 1  # Arguments *might* be in the eager extension
    OUT = 2  # Argument is defeated by an IN argument
    BLANK = 3  # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4  # Argument defeats IN argument
    UNDEC = 5  # Argument may not be included in the eager extension because not defended by any IN argument.


def get_eager_extension(argumentation_framework: AbstractArgumentationFramework) -> List[
    Set[Union[Any]]]:
    """
    Get the eager extension of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the eager extension.
    :return: eager extension of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> ees = get_eager_extension(af)
    >>> len(ees)
    1
    >>> frozenset({b, d}) in ees
    True
    >>> frozenset({b}) in ees
    False
    """
    initial_labelling = {argument: EagerExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    admissible_labellings = _recursively_get_admissible_labellings(argumentation_framework, initial_labelling, [])
    frozen_admissible_sets = set()
    for labelling in admissible_labellings:
        frozen_admissible_sets.add(frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                     if labelling[argument] == EagerExtensionLabel.IN})))
    admissible_sets = [set(frozen_admissible_set) for frozen_admissible_set in frozen_admissible_sets]
    calculated_eager_undec = []
    ss_labellings = []
    for ss_labelling in admissible_labellings:
        calculated_eager_undec.append([frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                         if ss_labelling[argument] == EagerExtensionLabel.UNDEC})),
                                       ss_labelling])
    for ss_labelling in admissible_labellings:
        candidate_eager_undec = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                  if ss_labelling[argument] == EagerExtensionLabel.UNDEC}))
        if not any(candidate_eager_undec > eager_undec[0]
                   for eager_undec in calculated_eager_undec):
            ss_labellings.append(ss_labelling)
            if any(candidate_eager_undec < eager_undec[0]
                   for eager_undec in calculated_eager_undec):
                for eager_undec in calculated_eager_undec:
                    if candidate_eager_undec < eager_undec[0] and eager_undec[1] in ss_labellings:
                        ss_labellings.remove(eager_undec[1])
    semistable_extensions = []
    for labelling in ss_labellings:
        semistable_extensions.append({argument for argument in argumentation_framework.arguments if
                                      labelling[argument] == EagerExtensionLabel.IN})
    intersect_semistable = set.intersection(*semistable_extensions)
    admissible_subsets = [admissible_set for admissible_set in admissible_sets if
                          intersect_semistable.issuperset(admissible_set) == True]
    max_admissible_subsets = []
    for candidate_eager_extension in admissible_subsets:
        if not any(candidate_eager_extension < admissible_set
                   for admissible_set in admissible_subsets):
            max_admissible_subsets.append(candidate_eager_extension)
    return max_admissible_subsets


def _recursively_get_admissible_labellings(argumentation_framework: AbstractArgumentationFramework,
                                           labelling: Dict[Argument, EagerExtensionLabel],
                                           admissible_labellings: List[Dict[Argument, EagerExtensionLabel]]) -> List[
    Dict[Argument, EagerExtensionLabel]]:
    if all(labelling[argument] != EagerExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != EagerExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            admissible_labellings.append(labelling)
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == EagerExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        admissible_sets = _recursively_get_admissible_labellings(argumentation_framework, alternative_labelling,
                                                                 admissible_labellings)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        admissible_sets = _recursively_get_admissible_labellings(argumentation_framework, alternative_labelling,
                                                                 admissible_labellings)
    return admissible_labellings


def _recursively_get_eager_extension(argumentation_framework: AbstractArgumentationFramework,
                                     labelling: Dict[Argument, EagerExtensionLabel],
                                     labellings) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != EagerExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != EagerExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_eager_undec = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                      if labelling[argument] == EagerExtensionLabel.UNDEC}))
            calculated_eager_undec = []
            for ss_labelling in labellings:
                calculated_eager_undec.append(
                    [frozenset(sorted({argument for argument in argumentation_framework.arguments
                                       if ss_labelling[argument] == EagerExtensionLabel.UNDEC})),
                     ss_labelling])
            if not any(candidate_eager_undec > eager_undec[0]
                       for eager_undec in calculated_eager_undec):
                labellings.append(labelling)
                if any(candidate_eager_undec < eager_undec[0]
                       for eager_undec in calculated_eager_undec):
                    for eager_undec in calculated_eager_undec:
                        if candidate_eager_undec < eager_undec[0]:
                            labellings.remove(eager_undec[1])
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == EagerExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        eager_extensions = _recursively_get_eager_extension(argumentation_framework, alternative_labelling,
                                                            labellings)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        eager_extensions = _recursively_get_eager_extension(argumentation_framework, alternative_labelling,
                                                            labellings)
    eager_extensions = set()
    for labelling in labellings:
        eager_extensions.add(frozenset(sorted({argument for argument in argumentation_framework.arguments if
                                               labelling[argument] == EagerExtensionLabel.IN})))

    return eager_extensions


def _in_trans(labelling: Dict[Argument, EagerExtensionLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, EagerExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = EagerExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = EagerExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != EagerExtensionLabel.OUT:
            new_labelling[defeated] = EagerExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, EagerExtensionLabel], argument: Argument) -> \
        Dict[Argument, EagerExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = EagerExtensionLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
