from typing import Dict

from py_arg.aspic_classes.orderings.democratic_ordering import DemocraticOrdering
from py_arg.aspic_classes.orderings.elitist_ordering import ElitistOrdering
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.instantiated_argument import InstantiatedArgument


class LastLinkOrdering(Ordering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)

    def argument_is_strictly_weaker_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        ldr_a = argument_a.last_defeasible_rules
        ldr_b = argument_b.last_defeasible_rules
        if self.rule_set_is_strictly_weaker_than(ldr_a, ldr_b):
            return True
        if len(ldr_a) == 0 and len(ldr_b) == 0 and self.ordinary_premise_set_is_strictly_weaker_than(
                argument_a.ordinary_premises, argument_b.ordinary_premises):
            return True
        return False

    def argument_is_weaker_or_equal_than(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        if self.argument_is_strictly_weaker_than(argument_a, argument_b):
            return True
        if len(argument_b.last_defeasible_rules) == 0:
            if argument_a.ordinary_premises == argument_b.ordinary_premises:
                return True
        else:
            if argument_a.last_defeasible_rules == argument_b.last_defeasible_rules:
                return True
        return False


class LastLinkDemocraticOrdering(DemocraticOrdering, LastLinkOrdering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)


class LastLinkElitistOrdering(ElitistOrdering, LastLinkOrdering):
    def __init__(self, defeasible_rule_preference_dict: Dict[str, Dict[str, Preference]],
                 ordinary_premise_preference_dict: Dict[str, Dict[str, Preference]]):
        super().__init__(defeasible_rule_preference_dict, ordinary_premise_preference_dict)
