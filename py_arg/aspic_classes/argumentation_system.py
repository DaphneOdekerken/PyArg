from typing import Dict, List, Optional, Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.strict_rule import StrictRule
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.literal import Literal


class ArgumentationSystem:
    def __init__(self,
                 language: Dict[str, Literal],
                 contraries_and_contradictories: Dict[str, Set[Literal]],
                 strict_rules: List[StrictRule],
                 defeasible_rules: List[DefeasibleRule],
                 defeasible_rule_preferences: Optional[List[Preference]] = None):
        # Language
        self.language = language

        # Contradiction function
        for literal_str, literal_contraries in contraries_and_contradictories.items():
            language[literal_str].contraries_and_contradictories = literal_contraries

        # Rules
        self.defeasible_rules = defeasible_rules
        self.strict_rules = strict_rules
        for defeasible_rule in defeasible_rules:
            defeasible_rule_literal = Literal.from_defeasible_rule(defeasible_rule)
            defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(defeasible_rule)
            defeasible_rule_literal.contraries_and_contradictories = {defeasible_rule_literal_negation}
            defeasible_rule_literal_negation.contraries_and_contradictories = {defeasible_rule_literal}
            language[str(defeasible_rule_literal)] = defeasible_rule_literal
            language[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation

        # Rule preferences
        self.rule_preference_dict = \
            {str(rule): {str(other_rule): Preference(str(rule), '?', str(other_rule))
                         for other_rule in self.defeasible_rules}
             for rule in self.defeasible_rules}
        if defeasible_rule_preferences is not None:
            for rule_preference in defeasible_rule_preferences:
                self.add_rule_preference(rule_preference)

    def get_literal(self, defeasible_rule: DefeasibleRule) -> Literal:
        return self.language[defeasible_rule.id_str]

    def __eq__(self, other):
        return self.language == other.language and self.defeasible_rules == other.defeasible_rules and \
               self.rule_preference_dict == other.rule_preference_dict

    def add_rule_preference(self, rule_preference: Preference):
        self.rule_preference_dict[str(rule_preference.object_a)][str(rule_preference.object_b)] = \
            rule_preference
        inverted_preference = Preference.inversion(rule_preference)
        self.rule_preference_dict[str(inverted_preference.object_a)][str(inverted_preference.object_b)] = \
            inverted_preference


if __name__ == "__main__":
    import doctest

    doctest.testmod()
