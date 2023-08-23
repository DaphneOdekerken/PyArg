import unittest

from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator


class TestAFGenerator(unittest.TestCase):
    def test_af_generator(self):
        generator = AbstractArgumentationFrameworkGenerator(3, 3, True)
        af = generator.generate()
        self.assertEqual(len(af.arguments), 3)
        self.assertEqual(len(af.defeats), 3)
