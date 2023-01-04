# from typing import Dict
#
# from py_arg.incomplete_argumentation_classes.argument_incomplete_argumentation_framework import \
#     ArgumentIncompleteArgumentationFramework
# from py_arg.aspic_classes.literal import Literal
# from py_arg.aspic_classes.orderings.ordering import Ordering
# from py_arg.incomplete_aspic_classes.potential_argument import PotentialArgument
# from py_arg.incomplete_aspic_classes.potential_argumentation_theory import PotentialArgumentationTheory
# from py_arg.labels.enum_stability_label import EnumStabilityLabel
# from py_arg.labels.potential_argument_label import PotentialArgumentLabel
#
#
# def potential_argument_based_stability_algorithm_from_potential_argumentation_theory(
#         potential_argumentation_theory: PotentialArgumentationTheory,
#         ordering: Ordering) -> Dict[PotentialArgument, PotentialArgumentLabel]:
#     incomplete_argumentation_framework = ArgumentIncompleteArgumentationFramework.from_potential_argumentation_theory(
#         '', potential_argumentation_theory, ordering)
#
#     arguments_in_ng, arguments_in_ang = incomplete_argumentation_framework.get_necessary_grounded_extension()
#     arguments_in_pg, arguments_in_apg = incomplete_argumentation_framework.get_possible_grounded_extension()
#
#     potential_argument_labels = {potential_argument: PotentialArgumentLabel()
#                                  for potential_argument in potential_argumentation_theory.all_potential_arguments}
#     for argument in potential_argumentation_theory.all_arguments:
#         potential_argument_labels[argument].in_arguments = True
#     for potential_argument in arguments_in_ng:
#         potential_argument_labels[potential_argument].in_necessary_grounded_extension = True
#     for potential_argument in arguments_in_ang:
#         potential_argument_labels[potential_argument].defeated_by_necessary_grounded_extension = True
#     for potential_argument in arguments_in_pg:
#         potential_argument_labels[potential_argument].in_possible_grounded_extension = True
#     for potential_argument in arguments_in_apg:
#         potential_argument_labels[potential_argument].defeated_by_possible_grounded_extension = True
#
#     return potential_argument_labels
#
#
# def from_potential_argument_labels_to_literal_labels(
#         potential_argument_labels: Dict[PotentialArgument, PotentialArgumentLabel], language: Dict[str, Literal]) -> \
#         Dict[Literal, EnumStabilityLabel]:
#     potential_argument_labels_per_literal = {literal: [] for literal in language.values()}
#     for potential_argument, potential_argument_label in potential_argument_labels.items():
#         potential_argument_labels_per_literal[potential_argument.conclusion].append(potential_argument_label)
#
#     labels = {}
#     for literal in language.values():
#         labels[literal] = EnumStabilityLabel.UNSTABLE
#         if not potential_argument_labels_per_literal[literal]:
#             labels[literal] = EnumStabilityLabel.UNSATISFIABLE
#         else:
#             pot_arg_labels = potential_argument_labels_per_literal[literal]
#             if any(pot_arg_label.in_necessary_grounded_extension for pot_arg_label in pot_arg_labels):
#                 labels[literal] = EnumStabilityLabel.DEFENDED
#             elif any(pot_arg_label.in_arguments for pot_arg_label in pot_arg_labels):
#                 if all(pot_arg_label.defeated_by_necessary_grounded_extension for pot_arg_label in pot_arg_labels):
#                     labels[literal] = EnumStabilityLabel.OUT
#                 elif all(not pot_arg_label.in_possible_grounded_extension and
#                          not pot_arg_label.defeated_by_possible_grounded_extension
#                          for pot_arg_label in pot_arg_labels):
#                     labels[literal] = EnumStabilityLabel.BLOCKED
#
#     return labels

# TODO onderstaande verwerken
# def get_possible_grounded_extension(self) -> Tuple[Set[Argument], Set[Argument]]:
#     all_certain_or_uncertain_arguments = list(self._uncertain_arguments.values()) + list(self._arguments.values())
#
#     pg = {argument for argument in all_certain_or_uncertain_arguments
#           if all(str(attacking_argument) not in self._arguments.keys()
#                  for attacking_argument in argument.get_ingoing_defeat_arguments)}
#     apg = {argument
#            for pg_argument in pg
#            for argument in pg_argument.get_outgoing_defeat_arguments
#            if argument.name in self._arguments}
#
#     change = True
#     while change:
#         new_in_pg = {argument for argument in all_certain_or_uncertain_arguments
#                      if argument not in pg and
#                      all(attacking_argument in apg
#                          for attacking_argument in argument.get_ingoing_defeat_arguments)}
#         if new_in_pg:
#             change = True
#             pg = pg | new_in_pg
#             apg = apg | {argument for pg_argument in pg for argument in pg_argument.get_outgoing_defeat_arguments
#                          if argument.name in self._arguments}
#         else:
#             change = False
#
#     return pg, apg
