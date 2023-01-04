# from typing import List
#
# from py_arg.abstract_argumentation_classes.argument import Argument
# from py_arg.incomplete_argumentation_classes.argument_incomplete_argumentation_framework import \
#     ArgumentIncompleteArgumentationFramework
#
#
# def get_relevant_uncertain_arguments_for_adding_to_ng(
#         argument: Argument,
#         incomplete_argumentation_framework: ArgumentIncompleteArgumentationFramework) -> List[Argument]:
#
#     ng, _ = incomplete_argumentation_framework.get_necessary_grounded_extension()
#
#     if argument in ng:
#         return []
#
#     relevant_list = []
#     attacking_potential_arguments = set(argument.get_ingoing_defeat_arguments)
#
#     while attacking_potential_arguments:
#         attacking_potential_argument = attacking_potential_arguments.pop()
#
#         possible_defenders = [att_att_pot_arg
#                               for att_att_pot_arg in attacking_potential_argument.get_ingoing_defeat_arguments
#                               if attacking_potential_argument not in att_att_pot_arg.get_ingoing_defeat_arguments]
#
#         if not possible_defenders:
#             return []
#
#         possible_not_yet_in_ng_defenders = [defender for defender in possible_defenders
#                                             if defender not in ng]
#
#         if possible_not_yet_in_ng_defenders:
#             possible_yet_unknown_defenders = \
#                 [defender for defender in possible_not_yet_in_ng_defenders
#                  if defender.name not in incomplete_argumentation_framework.arguments.keys()]
#             relevant_list += possible_yet_unknown_defenders
#
#             attacking_potential_arguments |= {defender_attacker for defender in possible_not_yet_in_ng_defenders
#                                               for defender_attacker in defender.get_ingoing_defeat_arguments}
#
#     return relevant_list
