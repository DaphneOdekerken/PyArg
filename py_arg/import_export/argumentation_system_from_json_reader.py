import json

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder
from py_arg.aspic_classes.strict_rule import StrictRule


class ArgumentationSystemFromJsonReader:
    def __init__(self):
        pass

    @staticmethod
    def from_json(json_object) -> ArgumentationSystem:
        language = {literal_str: Literal(literal_str) for literal_str in json_object['language']}
        contraries = {literal_str: {language[con_lit] for con_lit in con_lit_list}
                      for literal_str, con_lit_list in json_object['contraries'].items()}

        defeasible_rules = []
        for defeasible_rule_str in json_object['defeasible_rules']:
            antecedents_str, consequent_str = defeasible_rule_str[1].split('=>', 1)
            antecedent_str_list = antecedents_str.split(',')
            defeasible_rule = DefeasibleRule(defeasible_rule_str[0],
                                             {language[antecedent_str] for antecedent_str in antecedent_str_list},
                                             language[consequent_str])
            defeasible_rules.append(defeasible_rule)
        def_rules_lookup = {defeasible_rule.id: defeasible_rule for defeasible_rule in defeasible_rules}

        strict_rules = []
        for strict_rule_str in json_object['strict_rules']:
            antecedents_str, consequent_str = strict_rule_str[1].split('->', 1)
            antecedent_str_list = antecedents_str.split(',')
            strict_rule = StrictRule(strict_rule_str[0],
                                     {language[antecedent_str] for antecedent_str in antecedent_str_list},
                                     language[consequent_str])
            strict_rules.append(strict_rule)

        rule_preferences = PreferencePreorder()
        for rule_preference in json_object['rule_preferences']:
            rule_preferences.append((def_rules_lookup[rule_preference[0]], def_rules_lookup[rule_preference[1]]))

        return ArgumentationSystem(language, contraries, strict_rules, defeasible_rules, rule_preferences,
                                   add_defeasible_rule_literals=False)

    def read_from_json(self, file_path: str) -> ArgumentationSystem:
        with open(file_path, 'r') as reader:
            argumentation_system_json = json.load(reader)
        return self.from_json(argumentation_system_json)
