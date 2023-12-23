from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    ExtendedExtensionLabel


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne.
# "Algorithms for decision problems in argument systems
# under preferred semantics." Artificial Intelligence 207 (2014): 23-51.
# Adjustment based on Modgil, Sanjay and Martin Caminada. "Proof Theories and
# Algorithms for Abstract Argumentation
# Frameworks." In Iyad Rahwan and Guillermo R. Simari, editors, Argumentation
# in Artificial Intelligence, pages 105–132


def get_semistable_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[Argument]]:
    """
    Get the semi-stable extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
        need the semi-stable extensions.
    :return: semi-stable extension of the argumentation framework.
    """
    initial_labelling = {argument: ExtendedExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return _recursively_get_semistable_extensions(argumentation_framework,
                                                  initial_labelling, [])


def _recursively_get_semistable_extensions(
        argumentation_framework: AbstractArgumentationFramework,
        labelling: Dict[Argument, ExtendedExtensionLabel],
        labellings) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != ExtendedExtensionLabel.BLANK
           for argument in argumentation_framework.arguments):
        if all(labelling[argument] != ExtendedExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_semistable_undec = frozenset(sorted({
                argument for argument in argumentation_framework.arguments
                if labelling[argument] == ExtendedExtensionLabel.UNDEC}))
            calculated_semistable_undec = []
            for ss_labelling in labellings:
                calculated_semistable_undec.append(
                    [frozenset(sorted({
                        argument
                        for argument in argumentation_framework.arguments
                        if ss_labelling[argument] ==
                           ExtendedExtensionLabel.UNDEC})),
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
        blank_argument = \
            [argument for argument in argumentation_framework.arguments
             if labelling[argument] == ExtendedExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument,
                                          argumentation_framework)
        semistable_extensions = _recursively_get_semistable_extensions(
            argumentation_framework, alternative_labelling, labellings)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        semistable_extensions = _recursively_get_semistable_extensions(
            argumentation_framework, alternative_labelling, labellings)
    semistable_extensions = set()
    for labelling in labellings:
        semistable_extensions.add(frozenset(sorted({
            argument for argument in argumentation_framework.arguments
            if labelling[argument] == ExtendedExtensionLabel.IN})))

    return semistable_extensions


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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
