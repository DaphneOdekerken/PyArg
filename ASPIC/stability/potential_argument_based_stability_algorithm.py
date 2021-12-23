from ASPIC.abstract_argumentation_classes.argument_incomplete_argumentation_framework import \
    ArgumentIncompleteArgumentationFramework
from ASPIC.aspic_classes.ordering import Ordering
from ASPIC.dynamic_aspic_classes.potential_argumentation_theory import PotentialArgumentationTheory
from ASPIC.labels.enum_stability_label import EnumStabilityLabel
from ASPIC.labels.literal_labels import LiteralLabels


def potential_argument_based_stability_algorithm_from_potential_argumentation_theory(
        potential_argumentation_theory: PotentialArgumentationTheory,
        ordering: Ordering) -> LiteralLabels:
    incomplete_argumentation_framework = ArgumentIncompleteArgumentationFramework.from_potential_argumentation_theory(
        '', potential_argumentation_theory, ordering)

    arguments_in_ng, arguments_in_ang = incomplete_argumentation_framework.get_necessary_grounded_extension()
    arguments_in_pg, arguments_in_apg = incomplete_argumentation_framework.get_possible_grounded_extension()

    labels = {}
    for literal_str, literal in potential_argumentation_theory.argumentation_system.language.items():
        labels[literal] = EnumStabilityLabel.UNSTABLE
        if not potential_argumentation_theory.potential_arguments[literal]:
            labels[literal] = EnumStabilityLabel.UNSATISFIABLE
        elif potential_argumentation_theory.arguments[literal]:
            if any(argument_in_ng.conclusion == literal for argument_in_ng in arguments_in_ng):
                labels[literal] = EnumStabilityLabel.DEFENDED
            elif all(pot_arg in arguments_in_ang
                     for pot_arg in potential_argumentation_theory.potential_arguments[literal]):
                labels[literal] = EnumStabilityLabel.OUT
            elif all(arg not in arguments_in_pg and arg not in arguments_in_apg
                     for arg in potential_argumentation_theory.arguments[literal]):
                labels[literal] = EnumStabilityLabel.BLOCKED
    return LiteralLabels(labels)
