from typing import Set

from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.strict_rule import StrictRule


def get_closure(literals: Set[Literal], strict_rules: Set[StrictRule]):
    closure = literals.copy()
    change = True
    while change:
        change = False
        interesting_strict_rules = {strict_rule for strict_rule in strict_rules
                                    if strict_rule.consequent not in closure}
        for strict_rule in interesting_strict_rules:
            if all([antecedent in closure for antecedent in strict_rule.antecedents]):
                closure.add(strict_rule.consequent)
                change = True
    return closure
