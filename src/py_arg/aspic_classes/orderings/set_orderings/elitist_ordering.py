from typing import Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder


class ElitistOrdering(Ordering):
    def __init__(self, defeasible_rule_preferences: PreferencePreorder,
                 ordinary_premise_preferences: PreferencePreorder):
        super().__init__(defeasible_rule_preferences, ordinary_premise_preferences)

    def rule_set_is_strictly_weaker_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        if not rule_set_a:
            return False
        if not rule_set_b:
            return True
        return any([all([self.rule_is_strictly_weaker_than(rule_from_a, rule_from_b)
                         for rule_from_b in rule_set_b])
                    for rule_from_a in rule_set_a])

    def ordinary_premise_set_is_strictly_weaker_than(self, ordinary_premise_set_a: Set[Literal],
                                                     ordinary_premise_set_b: Set[Literal]):
        if not ordinary_premise_set_a:
            return False
        if not ordinary_premise_set_b:
            return True
        return any([all([self.ordinary_premise_is_strictly_weaker_than(ordinary_premise_from_a, ordinary_premise_from_b)
                         for ordinary_premise_from_b in ordinary_premise_set_b])
                    for ordinary_premise_from_a in ordinary_premise_set_a])
