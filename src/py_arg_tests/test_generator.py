import pathlib
import unittest

from src.py_arg.experiments.experiment_generate_incomplete_argumentation_theory import \
    instantiate_incomplete_argumentation_theory_generator
from src.py_arg.import_export.argumentation_system_from_json_reader import ArgumentationSystemFromJsonReader
from src.py_arg.import_export.argumentation_system_to_json_writer import ArgumentationSystemToJSONWriter
from src.py_arg.import_export.incomplete_argumentation_theory_from_json_reader import \
    IncompleteArgumentationTheoryFromJsonReader
from src.py_arg.import_export.incomplete_argumentation_theory_from_lp_file_reader import \
    IncompleteArgumentationTheoryFromLPFileReader
from src.py_arg.import_export.incomplete_argumentation_theory_to_json_writer import \
    IncompleteArgumentationTheoryToJSONWriter
from src.py_arg.import_export.incomplete_argumentation_theory_to_lp_file_writer import \
    IncompleteArgumentationTheoryToLPFileWriter


class TestGenerator(unittest.TestCase):
    def test_generator_returns_consistent_knowledge_base_without_duplicates(self):
        for _ in range(100):
            iat_generator = instantiate_incomplete_argumentation_theory_generator()
            iat = iat_generator.generate()
            axioms = iat.knowledge_base_axioms
            self.assertTrue(len(axioms) == len(set(axioms)))
            self.assertFalse(any(ax1 in ax2.contraries_and_contradictories for ax1 in axioms for ax2 in axioms))

    def test_generator_readers_and_writers(self):
        iat_generator = instantiate_incomplete_argumentation_theory_generator()
        iat = iat_generator.generate()
        iat_writer = IncompleteArgumentationTheoryToLPFileWriter()
        iat_writer.write(iat, 'generated_iat.lp')
        iat_lp_reader = IncompleteArgumentationTheoryFromLPFileReader()

        data_folder = pathlib.Path(__file__).parent.parent / 'py_arg' / 'experiments' / 'generated_data'
        read_iat_lp = iat_lp_reader.read_from_lp_file(str(data_folder / 'generated_iat.lp'))
        iat_json_writer = IncompleteArgumentationTheoryToJSONWriter()
        iat_json_writer.write(iat, 'generated_iat.json')
        as_writer = ArgumentationSystemToJSONWriter()
        as_writer.write(iat.argumentation_system, 'generated_as.json')
        as_reader = ArgumentationSystemFromJsonReader()
        read_as = as_reader.read_from_json(str(data_folder / 'generated_as.json'))
        iat_reader = IncompleteArgumentationTheoryFromJsonReader()
        read_iat = iat_reader.read_from_json(str(data_folder / 'generated_iat.json'))
        self.assertEqual(read_as, iat.argumentation_system)
        self.assertEqual(read_iat, iat)
        self.assertEqual(read_iat_lp, iat)
