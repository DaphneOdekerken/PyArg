from typing import Dict, Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.ordinary_premise import OrdinaryPremise
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.instantiated_argument import InstantiatedArgument


class Ordering:
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        self.defeasible_rule_preference_dict = defeasible_rule_preference_dict
        self.ordinary_premise_preference_dict = ordinary_premise_preference_dict

    def _get_rule_preference(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> Preference:
        return self.defeasible_rule_preference_dict[str(rule_a)][str(rule_b)]

    def rule_is_strictly_weaker_than(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> bool:
        return self._get_rule_preference(rule_a, rule_b).is_strictly_weaker

    def rule_is_strictly_stronger_than(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> bool:
        return self._get_rule_preference(rule_a, rule_b).is_strictly_stronger

    def rule_is_stronger_or_equal_than(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> bool:
        return self._get_rule_preference(rule_a, rule_b).is_stronger_or_equal

    def rule_is_weaker_or_equal_than(self, rule_a: DefeasibleRule, rule_b: DefeasibleRule) -> bool:
        return self._get_rule_preference(rule_a, rule_b).is_weaker_or_equal

    def _get_premise_preference(self, ordinary_premise_a: OrdinaryPremise, ordinary_premise_b: OrdinaryPremise):
        return self.ordinary_premise_preference_dict[str(ordinary_premise_a)][str(ordinary_premise_b)]

    def ordinary_premise_is_strictly_weaker_than(self, ordinary_premise_a: OrdinaryPremise,
                                                 ordinary_premise_b: OrdinaryPremise) -> bool:
        return self._get_premise_preference(ordinary_premise_a, ordinary_premise_b).is_strictly_weaker

    def ordinary_premise_is_strictly_stronger_than(self, ordinary_premise_a: OrdinaryPremise,
                                                   ordinary_premise_b: OrdinaryPremise) -> bool:
        return self._get_premise_preference(ordinary_premise_a, ordinary_premise_b).is_strictly_stronger

    def ordinary_premise_is_stronger_or_equal_than(self, ordinary_premise_a: OrdinaryPremise,
                                                   ordinary_premise_b: OrdinaryPremise) -> bool:
        return self._get_premise_preference(ordinary_premise_a, ordinary_premise_b).is_stronger_or_equal

    def ordinary_premise_is_weaker_or_equal_than(self, ordinary_premise_a: OrdinaryPremise,
                                                 ordinary_premise_b: OrdinaryPremise) -> bool:
        return self._get_premise_preference(ordinary_premise_a, ordinary_premise_b).is_weaker_or_equal

    def rule_set_is_strictly_weaker_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        pass

    def ordinary_premise_set_is_strictly_weaker_than(self, ordinary_premise_set_a: Set[OrdinaryPremise],
                                                     ordinary_premise_set_b: Set[OrdinaryPremise]):
        pass

    def rule_set_is_weaker_or_equal_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        return self.rule_set_is_strictly_weaker_than(rule_set_a, rule_set_b) or rule_set_a == rule_set_b

    def ordinary_premise_set_is_weaker_or_equal_than(self, ordinary_premise_set_a: Set[OrdinaryPremise],
                                                     ordinary_premise_set_b: Set[OrdinaryPremise]):
        return self.ordinary_premise_set_is_strictly_weaker_than(ordinary_premise_set_a, ordinary_premise_set_b) or \
               ordinary_premise_set_a == ordinary_premise_set_b

    def rule_set_is_strictly_stronger_than(self, rule_set_a: Set[DefeasibleRule], rule_set_b: Set[DefeasibleRule]):
        return self.rule_set_is_strictly_weaker_than(rule_set_b, rule_set_a)

    def ordinary_premise_set_is_strictly_stronger_than(self, ordinary_premise_set_a: Set[OrdinaryPremise],
                                                       ordinary_premise_set_b: Set[OrdinaryPremise]):
        return self.ordinary_premise_set_is_strictly_weaker_than(ordinary_premise_set_b, ordinary_premise_set_a)

    def argument_is_strictly_weaker_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        pass

    def argument_is_strictly_stronger_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        return self.argument_is_strictly_weaker_than(argument_b, argument_a)
