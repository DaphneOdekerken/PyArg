from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.incomplete_argumentation_theory_generators.incomplete_argumentation_theory_generator import \
    IncompleteArgumentationTheoryGenerator


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
    arg_sys, layered_language = layered_argumentation_system_generator.generate(return_layered_language=True)

    # Generate an incomplete argumentation theory, where only literals on the first layer can be queryable.
    positive_queryable_candidates = {arg_sys.language[str(literal).replace('-', '')] for literal in layered_language[0]}
    return IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=list(positive_queryable_candidates),
        queryable_literal_ratio=0.5,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )


if __name__ == "__main__":
    for nr_of_literals in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]:
        for nr_of_rules in [nr_of_literals / 2, nr_of_literals, 3 * nr_of_literals / 2]:
            generator = instantiate_incomplete_argumentation_theory_generator(nr_of_literals, nr_of_rules)
            for instance in range(50):
                iaf = generator.generate()
