import time

from py_arg.algorithms.justification.compute_all_literal_grounded_justification_status_fast import \
    compute_all_literal_grounded_justification_status_fast
from py_arg.algorithms.justification.compute_all_literal_grounded_justification_status_naive import \
    compute_all_literal_grounded_justification_status_naive
from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.argumentation_theory_generators.argumentation_theory_generator import \
    ArgumentationTheoryGenerator


def instantiate_argumentation_theory_generator():
    nr_of_literals = 800
    nr_of_rules = 500
    lasg = LayeredArgumentationSystemGenerator(nr_of_literals, nr_of_rules,
                                               rule_antecedent_distribution={1: 200, 2: 100, 3: 100, 4: 100},
                                               literal_layer_distribution={0: 300, 1: 200, 2: 100, 3: 100, 4: 100},
                                               strict_rule_ratio=0.4)
    arg_sys = lasg.generate()
    knowledge_literal_ratio = 0.3
    axiom_knowledge_ratio = 0.5
    atg = ArgumentationTheoryGenerator(arg_sys, knowledge_literal_ratio=knowledge_literal_ratio,
                                       axiom_knowledge_ratio=axiom_knowledge_ratio)
    return atg


def execute_grounded_labelling_experiment(argumentation_theory_generator: ArgumentationTheoryGenerator):
    for iteration in range(100):
        arg_theory = argumentation_theory_generator.generate()
        ordering = None

        for i in range(1):
            start_time = time.time()
            grounded_labelling_naive = compute_all_literal_grounded_justification_status_naive(arg_theory, ordering)
            end_time = time.time()
            grounded_labelling_naive_time = end_time - start_time
            print(f'Runtime naive: {grounded_labelling_naive_time}')

        for i in range(10):
            start_time = time.time()
            grounded_labelling_fast = compute_all_literal_grounded_justification_status_fast(arg_theory, ordering)
            end_time = time.time()
            grounded_labelling_fast_time = end_time - start_time
            print(f'Runtime fast: {grounded_labelling_fast_time}')

        if grounded_labelling_naive != grounded_labelling_fast:
            print('ERROR')


if __name__ == "__main__":
    atg = instantiate_argumentation_theory_generator()
    execute_grounded_labelling_experiment(atg)
