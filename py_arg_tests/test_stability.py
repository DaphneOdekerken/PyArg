import pathlib
import unittest
from typing import List

from py_arg.algorithms.stability.stability_labeler import StabilityLabeler
from py_arg.import_export.incomplete_argumentation_theory_from_xlsx_reader import \
    IncompleteArgumentationTheoryFromXLSXFileReader


def path_to_resources(filename: str):
    return pathlib.Path.cwd() / 'resources' / (filename + '.xlsx')


class TestStability(unittest.TestCase):
    def test_fraud_mini_test(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('03_2019_FQAS_Paper_Example'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['wrong_product'])
        stability_labels = stability_labeler.label(iat)
        self.assertFalse(stability_labels.literal_labeling[language['fraud']].is_stable)
        self.assertTrue(stability_labels.literal_labeling[language['fraud']].is_contested_stable)

        update_knowledge_base(['wrong_product', 'counter_party_delivered'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['fraud']].is_stable)

        update_knowledge_base(['counter_party_delivered'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['fraud']].is_contested_stable)

    def test_inconsistent_premise_test(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter01_inconsistent_premises'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()
        stability_labels = stability_labeler.label(iat)
        self.assertFalse(stability_labels.literal_labeling[language['t']].is_stable)

    def test_support_cycle(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter02_support_cycle'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_attack_cycle(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter03_attack_cycle'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o1', 'o2'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_ou_irrelevant_d_lit_c(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter04_OU_irrelevant_in_D_lit_c'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o1', 'o2'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_bou_irrelevant_b_lit_b(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter05_BOU_irrelevant_in_B_lit_b'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o1', 'o2', 'o5'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_db_irrelevant_b_lit_a(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter06_DB_irrelevant_in_B_lit_a'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o1'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_dbo_irrelevant_o_lit_a(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter07_DBO_irrelevant_in_O_lit_a'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o1', '-t'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_uo_irrelevant_o_lit_b(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter08_UO_irrelevant_in_O_lit_b'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o1', 'o2', 'o3'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_dbo_irrelevant_o_rule(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter09_DBO_irrelevant_in_O_rule'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o3', 'o4', 'o5'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_db_irrelevant_b_rule(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter10_DB_irrelevant_in_B_rule'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o2', 'o3', 'o4'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_support_cycle_attacker(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter11_support_cycle_attacker'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o'])
        stability_labels = stability_labeler.label(iat)
        self.assertTrue(stability_labels.literal_labeling[language['t']].is_stable)

    def test_support_cycle_attacker_q(self):
        asr = IncompleteArgumentationTheoryFromXLSXFileReader()
        iat = asr.read_from_xlsx_file(path_to_resources('counter12_support_cycle_attacker_q'))
        language = iat.argumentation_system.language
        stability_labeler = StabilityLabeler()

        def update_knowledge_base(str_list: List[str]):
            iat.knowledge_base_axioms = [iat.argumentation_system.language[lit_str] for lit_str in str_list]

        update_knowledge_base(['o'])
        stability_labels = stability_labeler.label(iat)
        self.assertFalse(stability_labels.literal_labeling[language['t']].is_stable)


if __name__ == '__main__':
    unittest.main()
