from typing import List

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.argument_incomplete_argumentation_framework import \
    ArgumentIncompleteArgumentationFramework


def get_relevant_uncertain_arguments_for_removing_from_pg(
        argument: Argument,
        incomplete_argumentation_framework: ArgumentIncompleteArgumentationFramework) -> List[Argument]:
    pg, _ = incomplete_argumentation_framework.get_possible_grounded_extension()

    def rel_given_pg(argument_from: Argument) -> List[Argument]:
        if argument_from not in pg:
            return []
        if not argument_from.get_ingoing_defeat_arguments:
            return []
        attackers_to_add = [att for att in argument_from.get_ingoing_defeat_arguments
                            if att.name not in incomplete_argumentation_framework.arguments.keys() and
                            not any(att_att.name in incomplete_argumentation_framework.arguments.keys()
                                    and att not in att_att.get_ingoing_defeat_arguments
                                    for att_att in att.get_ingoing_defeat_arguments)]
        if not attackers_to_add:
            attackers_to_add = [relevant_argument
                                for att in argument_from.get_ingoing_defeat_arguments
                                for att_att in argument_from.get_ingoing_defeat_arguments
                                if att not in att_att.get_ingoing_defeat_arguments
                                for relevant_argument in rel_given_pg(att_att)]

        return attackers_to_add

    return rel_given_pg(argument)
