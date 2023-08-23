import unittest

from py_arg.import_export.argumentation_framework_from_aspartix_format_reader import \
    ArgumentationFrameworkFromASPARTIXFormatReader


class TestAFFromAPX(unittest.TestCase):
    def test_af_from_apx(self):
        test_file_str = 'arg(A).\n' \
                        'arg(B).\n' \
                        'arg(C).\n' \
                        'att(A, B).\n' \
                        'att(B, C).\n' \
                        'att(B, A).\n'
        af = ArgumentationFrameworkFromASPARTIXFormatReader.from_apx(test_file_str)
        self.assertEqual(len(af.arguments), 3)
        self.assertEqual(len(af.defeats), 3)
