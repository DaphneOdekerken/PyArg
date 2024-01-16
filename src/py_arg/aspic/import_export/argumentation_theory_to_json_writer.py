import json

from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.import_export.argumentation_system_to_json_writer import \
    ArgumentationSystemToJSONWriter
from py_arg.incomplete_aspic.import_export.writer import Writer


class ArgumentationTheoryToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def to_dict(argumentation_theory: ArgumentationTheory):
        return {
            'argumentation_system': ArgumentationSystemToJSONWriter().to_dict(
                argumentation_theory.argumentation_system),
            'axioms': [str(literal)
                       for literal in
                       argumentation_theory.knowledge_base_axioms],
            'ordinary_premises':
                [str(literal)
                 for literal in argumentation_theory.
                 knowledge_base_ordinary_premises],
            'ordinary_premise_preferences':
                [(str(premise_preference_tuple[0]),
                  str(premise_preference_tuple[1]))
                 for premise_preference_tuple in
                 argumentation_theory.ordinary_premise_preferences.
                 preference_tuples]
        }

    def write(self, argumentation_theory: ArgumentationTheory, file_name: str):
        write_path = self.data_folder / file_name
        result = self.to_dict(argumentation_theory)
        with open(write_path, 'w') as write_file:
            json.dump(result, write_file)
