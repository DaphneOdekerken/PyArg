from typing import Dict

from ASPIC.aspic_classes.democratic_ordering import DemocraticOrdering
from ASPIC.aspic_classes.elitist_ordering import ElitistOrdering
from ASPIC.aspic_classes.ordering import Ordering
from ASPIC.aspic_classes.preference import Preference
from ASPIC.aspic_classes.instantiated_argument import InstantiatedArgument


class WeakestLinkOrdering(Ordering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)

    def argument_is_strictly_weaker_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        if argument_a.is_strict and argument_b.is_strict:
            return self.ordinary_premise_set_is_strictly_weaker_than(argument_a.ordinary_premises,
                                                                     argument_b.ordinary_premises)
        elif argument_a.is_firm and argument_b.is_firm:
            return self.rule_set_is_strictly_weaker_than(argument_a.defeasible_rules, argument_b.defeasible_rules)
        else:
            return self.ordinary_premise_set_is_strictly_weaker_than(
                argument_a.ordinary_premises, argument_b.ordinary_premises) and \
                   self.rule_set_is_strictly_weaker_than(argument_a.defeasible_rules, argument_b.defeasible_rules)

    def argument_is_weaker_or_equal_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        if self.argument_is_strictly_weaker_than(argument_a, argument_b):
            return True
        if argument_a.defeasible_rules == argument_b.defeasible_rules and \
                argument_a.ordinary_premises == argument_b.ordinary_premises:
            return True
        return False


class WeakestLinkDemocraticOrdering(DemocraticOrdering, WeakestLinkOrdering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)


class WeakestLinkElitistOrdering(ElitistOrdering, WeakestLinkOrdering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)
