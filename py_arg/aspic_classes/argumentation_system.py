from typing import Dict, List, Optional, Set

from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.strict_rule import StrictRule
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.literal import Literal


class ArgumentationSystem:
    def __init__(self,
                 language: Dict[str, Literal],
                 contraries: Dict[str, Set[Literal]],
                 strict_rules: List[StrictRule],
                 defeasible_rules: List[DefeasibleRule],
                 defeasible_rule_preferences: Optional[List[Preference]] = None):
        # Language
        self.language = language

        # Contradiction function
        for literal_str, literal_contraries in contraries.items():
            language[literal_str].contraries = literal_contraries

        # Rules
        self.defeasible_rules = defeasible_rules
        self.strict_rules = strict_rules

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

    def update_literal_name(self, old_literal_name: str, new_literal_name: str) -> None:
        """
        Change the name of a Literal in this ArgumentationSystem. Make sure that all connections are still correct.

        :param old_literal_name: The old name of the Literal.
        :param new_literal_name: The new name of the Literal.
        """
        if old_literal_name not in self.language.keys():
            raise ValueError(old_literal_name + ' was not a literal.')
        if new_literal_name in self.language.keys():
            raise ValueError(new_literal_name + ' already exists. You cannot overwrite an existing literal.')
        if '~' in new_literal_name:
            raise ValueError('A new literal literal name cannot contain the \'~\' character.')

        old_literal = self.language[old_literal_name]
        old_literal_negation = old_literal.negation
        old_literal_negation_name = str(old_literal_negation)

        old_literal.update_literal_name(new_literal_name)
        old_literal_negation.update_literal_name('~' + new_literal_name)

        del self.language[old_literal_name]
        del self.language[old_literal_negation_name]
        self.language[str(old_literal)] = old_literal
        self.language[str(old_literal.negation)] = old_literal.negation

    def update_literal_information(self, literal_name: str, new_literal_nl_true_value: str,
                                   new_literal_nl_unknown_value: str, new_literal_nl_false_value: str) -> None:
        """
        Update the information of a Literal in the ArgumentationSystem.

        :param literal_name: Name of the Literal that should be changed.
        :param new_literal_nl_true_value: New text in natural language stating that the Literal is present (defended).
        :param new_literal_nl_unknown_value: New text in natural language stating that the Literal is unknown.
        :param new_literal_nl_false_value: New text in natural language stating that the Literal is absent.
        """
        if literal_name not in self.language.keys():
            raise ValueError(literal_name + ' was not a literal in the language.')
        literal = self.language[literal_name]
        literal.update_literal_information(new_literal_nl_true_value, new_literal_nl_unknown_value,
                                           new_literal_nl_false_value)

    def add_rule_preference(self, rule_preference: Preference):
        self.rule_preference_dict[str(rule_preference.object_a)][str(rule_preference.object_b)] = \
            rule_preference
        inverted_preference = Preference.inversion(rule_preference)
        self.rule_preference_dict[str(inverted_preference.object_a)][str(inverted_preference.object_b)] = \
            inverted_preference


if __name__ == "__main__":
    import doctest

    doctest.testmod()
