from typing import Optional

from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.labels.enum_justification_label import EnumJustificationLabel
from py_arg.labels.literal_labels import LiteralLabels
from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension


def compute_all_literal_grounded_justification_status_naive(argumentation_theory: ArgumentationTheory,
                                                            ordering: Optional[Ordering] = None) -> LiteralLabels:
    result = {literal: EnumJustificationLabel.UNSATISFIABLE
              for literal in argumentation_theory.argumentation_system.language.values()}
    arg_framework = argumentation_theory.create_abstract_argumentation_framework('af', ordering)
    for argument in arg_framework.arguments:
        result[argument.conclusion] = EnumJustificationLabel.BLOCKED
    grounded_extension = get_grounded_extension(arg_framework)
    for grounded_argument in grounded_extension:
        result[grounded_argument.conclusion] = EnumJustificationLabel.DEFENDED
        for attacked_argument in grounded_argument.get_outgoing_defeat_arguments:
            result[attacked_argument.conclusion] = EnumJustificationLabel.OUT
    return LiteralLabels(result)
