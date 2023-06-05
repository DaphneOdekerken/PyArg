import json

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.import_export.writer import Writer


class ArgumentationSystemToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def to_dict(argumentation_system: ArgumentationSystem):
        return {'language': list(argumentation_system.language.keys()),
                'contraries': {lit_str: [str(con_lit) for con_lit in lit.contraries_and_contradictories]
                               for lit_str, lit in argumentation_system.language.items()},
                'defeasible_rules': [(defeasible_rule.id, str(defeasible_rule))
                                     for defeasible_rule in argumentation_system.defeasible_rules],
                'strict_rules': [(strict_rule.id, str(strict_rule))
                                 for strict_rule in argumentation_system.strict_rules],
                'rule_preferences': [(rule_preference_tuple[0].id, rule_preference_tuple[1].id)
                                     for rule_preference_tuple in
                                     argumentation_system.rule_preferences.preference_tuples]
                }

    def write(self, argumentation_system: ArgumentationSystem, file_name: str):
        write_path = self.data_folder / file_name
        result = self.to_dict(argumentation_system)
        with open(write_path, 'w') as write_file:
            json.dump(result, write_file)
