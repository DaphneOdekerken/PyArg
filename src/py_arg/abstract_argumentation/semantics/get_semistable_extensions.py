from typing import Set, Dict, FrozenSet, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    ExtendedExtensionLabel


# Algorithm for preferred semantics (Section 5.1), adapted as described in
# Section 6 in Sanjay Modgil and Martin Caminada.
# "Proof Theories and Algorithms for Abstract Argumentation Frameworks."
# In Argumentation in Artificial Intelligence (2009), 105–132

T = TypeVar('T', bound=Argument)


def get_semi_stable_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    """
    Get the semi-stable extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we
        need the semi-stable extensions.
    :return: semi-stable extension of the argumentation framework.
    """
    candidate_labellings = []
    initial_labelling = {argument: ExtendedExtensionLabel.IN
                         for argument in argumentation_framework.arguments}

    def _find_semi_stable_labellings(
            current_labelling: Dict[T, ExtendedExtensionLabel]):
        nonlocal candidate_labellings
        nonlocal argumentation_framework

        # Return if the UNDEC labels of some candidate labelling is a strict
        # subset of the UNDEC labels of the current labelling.
        current_undec_arguments = frozenset(sorted(
            {argument for argument in argumentation_framework.arguments
             if current_labelling[argument] == ExtendedExtensionLabel.UNDEC}))
        for other_labelling in candidate_labellings:
            other_undec_arguments = frozenset(sorted(
                {argument for argument in argumentation_framework.arguments
                 if
                 other_labelling[argument] == ExtendedExtensionLabel.UNDEC}))
            if other_undec_arguments < current_undec_arguments:
                return

        # Check if current_labelling has an argument that is illegally IN.
        illegally_in_arguments = {
            argument for argument in argumentation_framework.arguments
            if is_illegally_in(current_labelling, argument,
                               argumentation_framework)
        }

        if not illegally_in_arguments:
            new_candidate_labellings = []
            for candidate_labelling in candidate_labellings:
                # Only keep this candidate if the current labelling's UNDEC
                # arguments are not a strict super subset of the candidate's
                # UNDEC arguments.
                other_in_arguments = frozenset(sorted(
                    {argument for argument in argumentation_framework.arguments
                     if candidate_labelling[argument] ==
                     ExtendedExtensionLabel.UNDEC}))
                if not current_undec_arguments < other_in_arguments and \
                        candidate_labelling not in new_candidate_labellings:
                    new_candidate_labellings.append(candidate_labelling)

            # Also add the current candidate itself and return.
            new_candidate_labellings.append(current_labelling)
            candidate_labellings = new_candidate_labellings
            return
        else:
            # Try to find a super illegally IN argument in the current
            # labelling.
            super_illegally_in_argument = None
            for argument in argumentation_framework.arguments:
                if is_super_illegally_in(current_labelling, argument,
                                         argumentation_framework):
                    super_illegally_in_argument = argument
                    break

            if super_illegally_in_argument:
                new_labelling = transition_step(
                    current_labelling, super_illegally_in_argument,
                    argumentation_framework)
                _find_semi_stable_labellings(new_labelling)
            else:
                for illegally_in_argument in illegally_in_arguments:
                    new_labelling = transition_step(
                        current_labelling, illegally_in_argument,
                        argumentation_framework)
                    _find_semi_stable_labellings(new_labelling)

    _find_semi_stable_labellings(initial_labelling)
    return {
        frozenset(sorted(
            {argument for argument in argumentation_framework.arguments
             if labelling[argument] == ExtendedExtensionLabel.IN}))
        for labelling in candidate_labellings
    }


def is_illegally_in(
        labelling: Dict[T, ExtendedExtensionLabel],
        argument: T,
        argumentation_framework: AbstractArgumentationFramework
) -> bool:
    if not labelling[argument] == ExtendedExtensionLabel.IN:
        return False

    defeaters = argumentation_framework.get_incoming_defeat_arguments(argument)
    for defeater in defeaters:
        if labelling[defeater] != ExtendedExtensionLabel.OUT:
            return True

    return False


def is_legally_in(
        labelling: Dict[T, ExtendedExtensionLabel],
        argument: T,
        argumentation_framework: AbstractArgumentationFramework
) -> bool:
    if not labelling[argument] == ExtendedExtensionLabel.IN:
        return False

    defeaters = argumentation_framework.get_incoming_defeat_arguments(argument)
    for defeater in defeaters:
        if labelling[defeater] != ExtendedExtensionLabel.OUT:
            return False

    return True


def is_super_illegally_in(
        labelling: Dict[T, ExtendedExtensionLabel],
        argument: T,
        argumentation_framework: AbstractArgumentationFramework
) -> bool:
    if not labelling[argument] == ExtendedExtensionLabel.IN:
        return False

    defeaters = argumentation_framework.get_incoming_defeat_arguments(argument)
    for defeater in defeaters:
        if labelling[defeater] == ExtendedExtensionLabel.UNDEC:
            return True
        if is_legally_in(labelling, defeater, argumentation_framework):
            return True
    return False


def transition_step(
        labelling: Dict[T, ExtendedExtensionLabel],
        argument: T,
        argumentation_framework: AbstractArgumentationFramework) -> \
        Dict[T, ExtendedExtensionLabel]:
    # The label of the argument is changed from IN to OUT.
    new_labelling = labelling.copy()
    new_labelling[argument] = ExtendedExtensionLabel.OUT

    # Specific arguments that are illegally labelled OUT become UNDEC.
    arguments_to_check = [argument] + \
        argumentation_framework.get_outgoing_defeat_arguments(argument)
    for argument_to_check in arguments_to_check:
        if new_labelling[argument_to_check] == ExtendedExtensionLabel.OUT and \
            all(new_labelling[defeater] != ExtendedExtensionLabel.IN
                for defeater in argumentation_framework.
                get_incoming_defeat_arguments(argument_to_check)):
            new_labelling[argument_to_check] = ExtendedExtensionLabel.UNDEC
    return new_labelling
