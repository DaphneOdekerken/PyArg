from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.incomplete_argumentation_theory_generators.incomplete_argumentation_theory_generator import \
    IncompleteArgumentationTheoryGenerator


def instantiate_incomplete_argumentation_theory_generator():
    layered_argumentation_system_generator = \
        LayeredArgumentationSystemGenerator(nr_of_literals=80, nr_of_rules=50,
                                            rule_antecedent_distribution={1: 20, 2: 10, 3: 10, 4: 10},
                                            literal_layer_distribution={0: 30, 1: 20, 2: 10, 3: 10, 4: 10},
                                            strict_rule_ratio=0)

    # Generate the argumentation system, and keep the "layers" of literals.
    arg_sys, layered_language = layered_argumentation_system_generator.generate(return_layered_language=True)

    # Generate an incomplete argumentation theory, where only literals on the first layer can be queryable.
    positive_queryable_candidates = {arg_sys.language[str(literal).replace('-', '')] for literal in layered_language[0]}
    return IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=list(positive_queryable_candidates),
        queryable_literal_ratio=
            len(positive_queryable_candidates) / layered_argumentation_system_generator.nr_of_literals,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )

instantiate_incomplete_argumentation_theory_generator()

