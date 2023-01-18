import json

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.import_export.incomplete_argumentation_theory_writer import Writer


class ArgumentationSystemToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    def write(self, argumentation_system: ArgumentationSystem, file_name: str):
        write_path = self.data_folder / file_name

        result = {'language': list(argumentation_system.language.keys()),
                  'contraries': {lit_str: [str(con_lit) for con_lit in lit.contraries_and_contradictories]
                                 for lit_str, lit in argumentation_system.language.items()},
                  'defeasible_rules': [str(defeasible_rule)
                                       for defeasible_rule in argumentation_system.defeasible_rules],
                  'strict_rules': [str(strict_rule)
                                   for strict_rule in argumentation_system.strict_rules],
                  'rule_preferences': [str(rule_preference_tuple)
                                       for rule_preference_tuple in
                                       argumentation_system.rule_preferences.preference_tuples]}
        with open(write_path, 'w') as write_file:
            json.dump(result, write_file)
