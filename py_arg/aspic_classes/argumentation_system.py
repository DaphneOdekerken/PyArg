from typing import Dict, List, Optional, Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder
from py_arg.aspic_classes.rule import Rule
from py_arg.aspic_classes.strict_rule import StrictRule
from py_arg.aspic_classes.literal import Literal


class ArgumentationSystem:
    def __init__(self,
                 language: Dict[str, Literal],
                 contraries_and_contradictories: Dict[str, Set[Literal]],
                 strict_rules: List[StrictRule],
                 defeasible_rules: List[DefeasibleRule],
                 defeasible_rule_preferences: Optional[PreferencePreorder] = None,
                 add_defeasible_rule_literals: bool = True):
        # Language
        self.language = language

        # Contradiction function
        for literal_str, literal_contraries in contraries_and_contradictories.items():
            self.language[literal_str].contraries_and_contradictories = literal_contraries

        # Rules
        self.defeasible_rules = defeasible_rules
        self.strict_rules = strict_rules
        if add_defeasible_rule_literals:
            for defeasible_rule in defeasible_rules:
                defeasible_rule_literal = Literal.from_defeasible_rule(defeasible_rule)
                defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(defeasible_rule)
                defeasible_rule_literal.contraries_and_contradictories = {defeasible_rule_literal_negation}
                defeasible_rule_literal_negation.contraries_and_contradictories = {defeasible_rule_literal}
                self.language[str(defeasible_rule_literal)] = defeasible_rule_literal
                self.language[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation

        # Rule preferences
        if defeasible_rule_preferences:
            self.rule_preferences = defeasible_rule_preferences
        else:
            reflexive_order = [(rule_a, rule_a) for rule_a in self.defeasible_rules]
            self.rule_preferences = PreferencePreorder(reflexive_order)

    @property
    def rules(self):
        rules: List[Rule] = self.strict_rules + self.defeasible_rules
        return rules

    def get_literal(self, defeasible_rule: DefeasibleRule) -> Literal:
        return self.language[defeasible_rule.id_str]

    def __eq__(self, other):
        return isinstance(other, ArgumentationSystem) and self.language == other.language and \
            all(literal.contraries_and_contradictories == other.language[lit_str].contraries_and_contradictories
                for lit_str, literal in self.language.items()) and \
            self.defeasible_rules == other.defeasible_rules and \
            self.strict_rules == other.strict_rules and \
            self.rule_preferences == other.rule_preferences


if __name__ == "__main__":
    import doctest
    doctest.testmod()
