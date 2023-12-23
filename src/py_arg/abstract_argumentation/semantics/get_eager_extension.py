from typing import Set, Dict, FrozenSet, List, Union, Any

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    ExtendedExtensionLabel


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne.
# "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014):
# 23-51.
# Adjustment based on Modgil, Sanjay and Martin Caminada. "Proof Theories and
# Algorithms for Abstract Argumentation
# Frameworks." In Iyad Rahwan and Guillermo R. Simari, editors, Argumentation
# in Artificial Intelligence, pages 105–132


def get_eager_extension(
        argumentation_framework: AbstractArgumentationFramework) -> \
        List[Set[Union[Any]]]:
    """
    Get the eager extension of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
        need the eager extension.
    :return: eager extension of the argumentation framework.
    """
    initial_labelling = {argument: ExtendedExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    admissible_labellings = _recursively_get_admissible_labellings(
        argumentation_framework, initial_labelling, [])
    frozen_admissible_sets = set()
    for labelling in admissible_labellings:
        frozen_admissible_sets.add(frozenset(sorted(
            {argument for argument in argumentation_framework.arguments
             if labelling[argument] == ExtendedExtensionLabel.IN})))
    admissible_sets = [set(frozen_admissible_set)
                       for frozen_admissible_set in frozen_admissible_sets]
    calculated_eager_undec = []
    ss_labellings = []
    for ss_labelling in admissible_labellings:
        calculated_eager_undec.append([frozenset(sorted(
            {argument for argument in argumentation_framework.arguments
             if ss_labelling[argument] == ExtendedExtensionLabel.UNDEC})),
                                       ss_labelling])
    for ss_labelling in admissible_labellings:
        candidate_eager_undec = frozenset(sorted({
            argument for argument in argumentation_framework.arguments
            if ss_labelling[argument] == ExtendedExtensionLabel.UNDEC}))
        if not any(candidate_eager_undec > eager_undec[0]
                   for eager_undec in calculated_eager_undec):
            ss_labellings.append(ss_labelling)
            if any(candidate_eager_undec < eager_undec[0]
                   for eager_undec in calculated_eager_undec):
                for eager_undec in calculated_eager_undec:
                    if candidate_eager_undec < eager_undec[0] and \
                            eager_undec[1] in ss_labellings:
                        ss_labellings.remove(eager_undec[1])
    semistable_extensions = []
    for labelling in ss_labellings:
        semistable_extensions.append({
            argument for argument in argumentation_framework.arguments
            if labelling[argument] == ExtendedExtensionLabel.IN})
    intersect_semistable = set.intersection(*semistable_extensions)
    admissible_subsets = [admissible_set
                          for admissible_set in admissible_sets if
                          intersect_semistable.issuperset(admissible_set)]
    max_admissible_subsets = []
    for candidate_eager_extension in admissible_subsets:
        if not any(candidate_eager_extension < admissible_set
                   for admissible_set in admissible_subsets):
            max_admissible_subsets.append(candidate_eager_extension)
    return max_admissible_subsets


def _recursively_get_admissible_labellings(
        argumentation_framework: AbstractArgumentationFramework,
        labelling: Dict[Argument, ExtendedExtensionLabel],
        admissible_labellings: List[Dict[Argument, ExtendedExtensionLabel]]) -> \
        List[Dict[Argument, ExtendedExtensionLabel]]:
    if all(labelling[argument] != ExtendedExtensionLabel.BLANK
           for argument in argumentation_framework.arguments):
        if all(labelling[argument] != ExtendedExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            admissible_labellings.append(labelling)
    return admissible_labellings


def _recursively_get_eager_extension(
        argumentation_framework: AbstractArgumentationFramework,
        labelling: Dict[Argument, ExtendedExtensionLabel],
        labellings) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != ExtendedExtensionLabel.BLANK
           for argument in argumentation_framework.arguments):
        if all(labelling[argument] != ExtendedExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_eager_undec = frozenset(sorted({
                argument for argument in argumentation_framework.arguments
                if labelling[argument] == ExtendedExtensionLabel.UNDEC}))
            calculated_eager_undec = []
            for ss_labelling in labellings:
                calculated_eager_undec.append(
                    [frozenset(sorted({
                        argument
                        for argument in argumentation_framework.arguments
                        if ss_labelling[argument] ==
                           ExtendedExtensionLabel.UNDEC})),
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
        blank_argument = \
            [argument for argument in argumentation_framework.arguments
             if labelling[argument] == ExtendedExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument,
                                          argumentation_framework)
        eager_extensions = _recursively_get_eager_extension(
            argumentation_framework, alternative_labelling, labellings)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        eager_extensions = _recursively_get_eager_extension(
            argumentation_framework, alternative_labelling, labellings)
    eager_extensions = set()
    for labelling in labellings:
        eager_extensions.add(frozenset(sorted({
            argument for argument in argumentation_framework.arguments
            if labelling[argument] == ExtendedExtensionLabel.IN})))

    return eager_extensions


def _in_trans(labelling: Dict[Argument, ExtendedExtensionLabel],
              argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> \
        Dict[Argument, ExtendedExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = ExtendedExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(
            argument):
        if defeater == argument:
            break
        else:
            new_labelling[defeater] = ExtendedExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(
            argument):
        if new_labelling[defeated] != ExtendedExtensionLabel.OUT:
            new_labelling[defeated] = ExtendedExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, ExtendedExtensionLabel],
                 argument: Argument) -> \
        Dict[Argument, ExtendedExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = ExtendedExtensionLabel.UNDEC
    return new_labelling
