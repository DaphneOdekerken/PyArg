from typing import Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.instantiated_argument import InstantiatedArgument
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder


class Ordering:
    def __init__(self, defeasible_rule_preferences: PreferencePreorder,
                 ordinary_premise_preferences: PreferencePreorder):
        self.defeasible_rule_preferences = defeasible_rule_preferences
        self.ordinary_premise_preferences = ordinary_premise_preferences

    def rule_is_strictly_weaker_than(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> bool:
        return self.defeasible_rule_preferences.is_strictly_weaker_than(rule_a, rule_b)

    def rule_is_weaker_or_equal_than(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> bool:
        return self.defeasible_rule_preferences.is_weaker_than(rule_a, rule_b)

    def ordinary_premise_is_strictly_weaker_than(self, ordinary_premise_a: Literal,
                                                 ordinary_premise_b: Literal) -> bool:
        return self.ordinary_premise_preferences.is_strictly_weaker_than(ordinary_premise_a, ordinary_premise_b)

    def ordinary_premise_is_weaker_or_equal_than(self, ordinary_premise_a: Literal,
                                                 ordinary_premise_b: Literal) -> bool:
        return self.ordinary_premise_preferences.is_weaker_than(ordinary_premise_a, ordinary_premise_b)

    def rule_set_is_strictly_weaker_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        pass

    def ordinary_premise_set_is_strictly_weaker_than(self, ordinary_premise_set_a: Set[Literal],
                                                     ordinary_premise_set_b: Set[Literal]):
        pass

    def rule_set_is_weaker_or_equal_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        return self.rule_set_is_strictly_weaker_than(rule_set_a, rule_set_b) or rule_set_a == rule_set_b

    def ordinary_premise_set_is_weaker_or_equal_than(self, ordinary_premise_set_a: Set[Literal],
                                                     ordinary_premise_set_b: Set[Literal]):
        return self.ordinary_premise_set_is_strictly_weaker_than(ordinary_premise_set_a, ordinary_premise_set_b) or \
               ordinary_premise_set_a == ordinary_premise_set_b

    def argument_is_strictly_weaker_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        pass
