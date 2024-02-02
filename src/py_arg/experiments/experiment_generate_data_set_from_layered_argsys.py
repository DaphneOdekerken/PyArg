from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.incomplete_argumentation_theory_generators.incomplete_argumentation_theory_generator import \
    IncompleteArgumentationTheoryGenerator
from py_arg.import_export.incomplete_argumentation_theory_to_lp_file_writer import \
    IncompleteArgumentationTheoryToLPFileWriter


def instantiate_incomplete_argumentation_theory_generator(nr_of_literals, nr_of_rules):
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
        LayeredArgumentationSystemGenerator(nr_of_literals=nr_of_literals,
                                            nr_of_rules=nr_of_rules,
                                            rule_antecedent_distribution=rule_antecedent_distribution,
                                            literal_layer_distribution=literal_layer_distribution,
                                            strict_rule_ratio=0)

    # Generate the argumentation system, and keep the "layers" of literals.
    arg_sys, layered_language = layered_argumentation_system_generator.generate(return_layered_language=True,
                                                                                add_rule_preferences=True)

    # Generate an incomplete argumentation theory, where only literals on the first layer can be queryable.
    positive_queryable_candidates = {arg_sys.language[str(literal).replace('-', '')] for literal in layered_language[0]}
    topics = list({str(literal) for literal in layered_language[3] + layered_language[4]})
    return IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=list(positive_queryable_candidates),
        queryable_literal_ratio=0.5,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    ), topics


literal_sizes = [7500, 10000]
rule_literal_ratios = [0.5, 1, 1.5]

for literal_size in literal_sizes:
    for rule_literal_ratio in rule_literal_ratios:
        rule_size = int(rule_literal_ratio * literal_size)
        for arg_sys_nr in range(5):
            generator, topic_literals = instantiate_incomplete_argumentation_theory_generator(literal_size, rule_size)
            for iat_nr in range(5):
                iat = generator.generate()
                IncompleteArgumentationTheoryToLPFileWriter().write(
                    incomplete_argumentation_theory=iat,
                    file_name=f'DS2_{str(literal_size)}L{str(rule_size)}R_AS{str(arg_sys_nr)}_IAT{str(iat_nr)}.pl',
                    topic_literals=topic_literals)
