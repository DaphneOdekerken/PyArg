import json

from py_arg.import_export.argumentation_system_to_json_writer import ArgumentationSystemToJSONWriter
from py_arg.import_export.writer import Writer
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class IncompleteArgumentationTheoryToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def to_dict(incomplete_argumentation_theory: IncompleteArgumentationTheory):
        return {'argumentation_system': ArgumentationSystemToJSONWriter().to_dict(
                    incomplete_argumentation_theory.argumentation_system),
                'axioms': [str(literal) for literal in incomplete_argumentation_theory.knowledge_base_axioms],
                'ordinary_premises':
                    [str(literal) for literal in incomplete_argumentation_theory.knowledge_base_ordinary_premises],
                'ordinary_premise_preferences':
                    [(str(premise_preference_tuple[0]), str(premise_preference_tuple[1]))
                     for premise_preference_tuple in
                     incomplete_argumentation_theory.ordinary_premise_preferences.preference_tuples],
                'queryables': [str(literal) for literal in incomplete_argumentation_theory.queryables]
                }

    def write(self, incomplete_argumentation_theory: IncompleteArgumentationTheory, file_name: str):
        write_path = self.data_folder / file_name
        result = self.to_dict(incomplete_argumentation_theory)
        with open(write_path, 'w') as write_file:
            json.dump(result, write_file)
