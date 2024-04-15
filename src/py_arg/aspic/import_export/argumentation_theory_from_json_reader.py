import json

from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.classes.orderings.preference_preorder import \
    PreferencePreorder
from py_arg.aspic.import_export.argumentation_system_from_json_reader import \
    ArgumentationSystemFromJsonReader


class ArgumentationTheoryFromJsonReader:
    def __init__(self):
        pass

    @staticmethod
    def from_json(json_object) -> ArgumentationTheory:
        argumentation_system = ArgumentationSystemFromJsonReader().from_json(
            json_object['argumentation_system'])
        knowledge_base_axioms = [argumentation_system.language[axiom_str]
                                 for axiom_str in json_object['axioms']]
        knowledge_base_ordinary_premises = [
            argumentation_system.language[prem_str]
            for prem_str in json_object['ordinary_premises']]
        ordinary_premise_preferences = PreferencePreorder(
            [(argumentation_system.language[lit_a],
              argumentation_system.language[lit_b])
             for lit_a, lit_b in json_object['ordinary_premise_preferences']])

        return ArgumentationTheory(
            argumentation_system, knowledge_base_axioms,
            knowledge_base_ordinary_premises, ordinary_premise_preferences)

    def read_from_json(self, file_path: str) -> ArgumentationTheory:
        with open(file_path, 'r') as reader:
            argumentation_theory_json = json.load(reader)
        return self.from_json(argumentation_theory_json)
