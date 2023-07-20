from typing import Set

from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.strict_rule import StrictRule
from py_arg.logic.closure import get_closure


def is_c_consistent(literals: Set[Literal], strict_rules: Set[StrictRule]) -> bool:
    closure = get_closure(literals, strict_rules)
    return any(literal_a in literal_b.contraries_and_contradictories for literal_a in closure for literal_b in closure)
