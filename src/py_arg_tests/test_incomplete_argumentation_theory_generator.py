import pathlib
import unittest

from py_arg.aspic.generators.argumentation_system_generators.\
    layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.incomplete_aspic.generators.\
    incomplete_argumentation_theory_generator import \
    IncompleteArgumentationTheoryGenerator
from py_arg.aspic.import_export.argumentation_system_from_json_reader \
    import ArgumentationSystemFromJsonReader
from py_arg.aspic.import_export.argumentation_system_to_json_writer \
    import ArgumentationSystemToJSONWriter
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_from_json_reader import \
    IncompleteArgumentationTheoryFromJsonReader
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_from_lp_file_reader import \
    IncompleteArgumentationTheoryFromLPFileReader
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_to_json_writer import \
    IncompleteArgumentationTheoryToJSONWriter
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_to_lp_file_writer import \
    IncompleteArgumentationTheoryToLPFileWriter


def instantiate_incomplete_argumentation_theory_generator():
    nr_of_literals = 100
    nr_of_rules = 150
    rule_antecedent_distribution = {1: int(nr_of_rules / 3),
                                    2: int(nr_of_rules / 3),
                                    3: int(nr_of_rules / 9),
                                    4: int(nr_of_rules / 9)}
    rules_left = nr_of_rules - sum(rule_antecedent_distribution.values())
    rule_antecedent_distribution[5] = rules_left

    literal_layer_distribution = {0: 2 * nr_of_literals / 3,
                                  1: nr_of_literals / 10,
                                  2: nr_of_literals / 10,
                                  3: nr_of_literals / 10}
    literals_left = nr_of_literals - sum(literal_layer_distribution.values())
    literal_layer_distribution[4] = literals_left

    layered_argumentation_system_generator = \
        LayeredArgumentationSystemGenerator(
            nr_of_literals=nr_of_literals, nr_of_rules=nr_of_rules,
            rule_antecedent_distribution=rule_antecedent_distribution,
            literal_layer_distribution=literal_layer_distribution,
            strict_rule_ratio=0)

    # Generate the argumentation system, and keep the "layers" of literals.
    arg_sys, layered_language = \
        layered_argumentation_system_generator.generate(
            return_layered_language=True)

    # Generate an incomplete argumentation theory, where only literals on the
    # first layer can be queryable.
    positive_queryable_candidates = \
        {arg_sys.language[str(literal).replace('-', '')]
         for literal in layered_language[0]}
    return IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=list(positive_queryable_candidates),
        queryable_literal_ratio=0.5,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )


class TestGenerator(unittest.TestCase):
    def test_generator_returns_consistent_knowledge_base_without_duplicates(
            self):
        for _ in range(10):
            iat_generator = \
                instantiate_incomplete_argumentation_theory_generator()
            iat = iat_generator.generate()
            axioms = iat.knowledge_base_axioms
            self.assertTrue(len(axioms) == len(set(axioms)))
            self.assertFalse(any(
                ax1 in ax2.contraries_and_contradictories
                for ax1 in axioms for ax2 in axioms))

    def test_generator_readers_and_writers(self):
        iat_generator = instantiate_incomplete_argumentation_theory_generator()
        iat = iat_generator.generate()
        iat_writer = IncompleteArgumentationTheoryToLPFileWriter()
        iat_writer.write(iat, 'generated_iat.lp')
        iat_lp_reader = IncompleteArgumentationTheoryFromLPFileReader()

        data_folder = pathlib.Path(__file__).parent.parent / \
            'py_arg' / 'experiments' / 'generated_data'
        read_iat_lp = iat_lp_reader.read_from_lp_file(
            str(data_folder / 'generated_iat.lp'))
        iat_json_writer = IncompleteArgumentationTheoryToJSONWriter()
        iat_json_writer.write(iat, 'generated_iat.json')
        as_writer = ArgumentationSystemToJSONWriter()
        as_writer.write(iat.argumentation_system, 'generated_as.json')
        as_reader = ArgumentationSystemFromJsonReader()
        read_as = as_reader.read_from_json(
            str(data_folder / 'generated_as.json'))
        iat_reader = IncompleteArgumentationTheoryFromJsonReader()
        read_iat = iat_reader.read_from_json(
            str(data_folder / 'generated_iat.json'))
        self.assertEqual(read_as, iat.argumentation_system)
        self.assertEqual(read_iat, iat)
        self.assertEqual(read_iat_lp, iat)
