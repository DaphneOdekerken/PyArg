from typing import Optional, List

from py_arg.import_export.writer import Writer
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class IncompleteArgumentationTheoryToLPFileWriter(Writer):
    def __init__(self):
        super().__init__()

    def write(self, incomplete_argumentation_theory: IncompleteArgumentationTheory, file_name: str,
              topic_literals: Optional[List[str]] = None):
        write_path = self.data_folder / file_name
        with open(write_path, 'w') as write_file:
            for queryable in incomplete_argumentation_theory.positive_queryables:
                write_file.write(f'queryable({queryable.s1.lower()}).\n')
            write_file.write('\n')

            for axiom in incomplete_argumentation_theory.knowledge_base_axioms:
                write_file.write(f'axiom({axiom.s1.lower()}).\n')
            write_file.write('\n')

            for literal in incomplete_argumentation_theory.argumentation_system.language.values():
                if literal.s1[0] != '-':
                    for contrary in literal.contraries_and_contradictories:
                        write_file.write(f'neg({literal.s1.lower()}, {contrary.s1.lower()}).\n')
            write_file.write('\n')

            for rule in incomplete_argumentation_theory.argumentation_system.defeasible_rules:
                id_rule = rule.id
                for antecedent in rule.antecedents:
                    write_file.write(f'body({str(id_rule)}, {antecedent.s1.lower()}).\n')
                write_file.write(f'head({str(id_rule)}, {rule.consequent.s1.lower()}).\n')
            write_file.write('\n')

            for (r1, r2) in incomplete_argumentation_theory.argumentation_system.rule_preferences.preference_tuples:
                write_file.write(f'preferred({r1.id}, {r2.id}).\n')
            write_file.write('\n')

            if topic_literals:
                for topic_literal in topic_literals:
                    write_file.write(f'topic({topic_literal.lower()}).\n')
