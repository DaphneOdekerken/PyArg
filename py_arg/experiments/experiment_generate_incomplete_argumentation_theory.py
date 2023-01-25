import pathlib

from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.incomplete_argumentation_theory_generators.incomplete_argumentation_theory_generator import \
    IncompleteArgumentationTheoryGenerator
from py_arg.import_export.argumentation_system_from_json_reader import ArgumentationSystemFromJsonReader
from py_arg.import_export.argumentation_system_to_json_writer import ArgumentationSystemToJSONWriter
from py_arg.import_export.incomplete_argumentation_theory_from_json_reader import \
    IncompleteArgumentationTheoryFromJsonReader
from py_arg.import_export.incomplete_argumentation_theory_from_lp_file_reader import \
    IncompleteArgumentationTheoryFromLPFileReader
from py_arg.import_export.incomplete_argumentation_theory_to_json_writer import \
    IncompleteArgumentationTheoryToJSONWriter
from py_arg.import_export.incomplete_argumentation_theory_to_lp_file_writer import \
    IncompleteArgumentationTheoryToLPFileWriter


def instantiate_incomplete_argumentation_theory_generator():
    layered_argumentation_system_generator = \
        LayeredArgumentationSystemGenerator(nr_of_literals=80, nr_of_rules=50,
                                            rule_antecedent_distribution={1: 20, 2: 10, 3: 10, 4: 10},
                                            literal_layer_distribution={0: 30, 1: 20, 2: 10, 3: 10, 4: 10},
                                            strict_rule_ratio=0)

    # Generate the argumentation system, and keep the "layers" of literals.
    arg_sys, layered_language = layered_argumentation_system_generator.generate(return_layered_language=True)

    # Generate an incomplete argumentation theory, where only literals on the first layer can be queryable.
    positive_queryable_candidates = [arg_sys.language[str(literal).replace('-', '')] for literal in layered_language[0]]
    return IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=positive_queryable_candidates,
        queryable_literal_ratio=0.3,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )


iat_generator = instantiate_incomplete_argumentation_theory_generator()
iat = iat_generator.generate()
iat_writer = IncompleteArgumentationTheoryToLPFileWriter()
iat_writer.write(iat, 'generated_iat.lp')
iat_lp_reader = IncompleteArgumentationTheoryFromLPFileReader()
read_iat_lp = iat_lp_reader.read_from_lp_file(str(pathlib.Path('generated_data') / 'generated_iat.lp'))
iat_json_writer = IncompleteArgumentationTheoryToJSONWriter()
iat_json_writer.write(iat, 'generated_iat.json')
as_writer = ArgumentationSystemToJSONWriter()
as_writer.write(iat.argumentation_system, 'generated_as.json')
as_reader = ArgumentationSystemFromJsonReader()
read_as = as_reader.read_from_json(str(pathlib.Path('generated_data') / 'generated_as.json'))
iat_reader = IncompleteArgumentationTheoryFromJsonReader()
read_iat = iat_reader.read_from_json(str(pathlib.Path('generated_data') / 'generated_iat.json'))
print(read_as == iat.argumentation_system)
print(read_iat == iat)
print(read_iat_lp == iat)
