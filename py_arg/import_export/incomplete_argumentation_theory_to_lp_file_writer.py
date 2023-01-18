from py_arg.import_export.incomplete_argumentation_theory_writer import IncompleteArgumentationTheoryWriter
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class IncompleteArgumentationTheoryToLPFileWriter(IncompleteArgumentationTheoryWriter):
    def __init__(self):
        super().__init__()

    def write(self, incomplete_argumentation_theory: IncompleteArgumentationTheory, file_name: str):
        write_path = self.data_folder / file_name
        with open(write_path, 'w') as write_file:
            for axiom in incomplete_argumentation_theory.knowledge_base_axioms:
                write_file.write(f'queryable({axiom.s1.replace("-", "")}).\n')
            write_file.write('\n')

            for literal in incomplete_argumentation_theory.argumentation_system.language.values():
                if literal.s1[0] != '-':
                    for contrary in literal.contraries_and_contradictories:
                        write_file.write(f'neg({literal.s1}, {contrary.s1}).\n')
            write_file.write('\n')

            for id_rule, rule in enumerate(incomplete_argumentation_theory.argumentation_system.defeasible_rules):
                for antecedent in rule.antecedents:
                    write_file.write(f'body({str(id_rule)}, {antecedent.s1}).\n')
                write_file.write(f'head({str(id_rule)}, {rule.consequent.s1}).\n')
