from typing import Dict, Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.aspic_classes.preference import Preference


class DemocraticOrdering(Ordering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)

    def rule_set_is_strictly_weaker_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        if len(rule_set_a) == 0:
            return False
        if len(rule_set_b) == 0:
            return True
        return all([any([self.rule_is_strictly_weaker_than(rule_from_a, rule_from_b)
                         for rule_from_b in rule_set_b])
                    for rule_from_a in rule_set_a])

    def ordinary_premise_set_is_strictly_weaker_than(self, ordinary_premise_set_a: Set[Literal],
                                                     ordinary_premise_set_b: Set[Literal]):
        if len(ordinary_premise_set_a) == 0:
            return False
        if len(ordinary_premise_set_b) == 0:
            return True
        return all([any([self.ordinary_premise_is_strictly_weaker_than(ordinary_premise_from_a, ordinary_premise_from_b)
                         for ordinary_premise_from_b in ordinary_premise_set_b])
                    for ordinary_premise_from_a in ordinary_premise_set_a])
