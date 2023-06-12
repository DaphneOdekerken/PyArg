from typing import List

from src.py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions
from src.py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from src.py_arg_learning.abstract_exercise_set import AbstractExerciseSet


class ListCompleteExtensions(AbstractExerciseSet):
    def get_explanation_html(self):
        return "A complete extension is a set of arguments that contains exactly those arguments that it defends."

    def generate_exercise_and_solutions(self, color_blind_mode: bool):
        argumentation_framework_generator = AbstractArgumentationFrameworkGenerator(4, 5, False)
        af = argumentation_framework_generator.generate()

        exercise_instance = self.argumentation_framework_to_exercise_instance(af)
        graph_data = self.argumentation_framework_to_graph_data(af, color_blind_mode)

        complete_extensions = get_complete_extensions(af)
        complete_extensions_str_list = \
            sorted([','.join(sorted(argument.name for argument in extension))
                    for extension in complete_extensions])

        solutions = complete_extensions_str_list
        return exercise_instance, graph_data, solutions

    def render_exercise_instance_text(self, exercise_instance):
        exercise_instance_parts = exercise_instance.split(';')
        exercise_text = 'Consider an abstract argumentation framework AF = (A, R) with A = {{{a}}} and R = {{{r}}}. ' \
                        'List all complete extensions. Use a new line for each set, and ' \
                        'represent a set with arguments X, Y and Z as {{X, Y, Z}}.'.format(
                                a=exercise_instance_parts[0],
                                r=exercise_instance_parts[1])
        return exercise_text

    def get_feedback(self, solution_by_user: str, pre_generated_solutions: List[str]):
        solutions_learner = solution_by_user.upper()

        def preprocess(input_str: str) -> List[str]:
            for c in '{}[]':
                input_str = input_str.replace(c, '')
            output_unsorted = [solution_part.strip() for solution_part in input_str.upper().split(',')]
            return sorted(output_unsorted)

        solutions_learner_parts = [preprocess(part) for part in solutions_learner.split('\n')]
        ground_truth_parts = [preprocess(part) for part in pre_generated_solutions]

        overlapping_parts = [part for part in solutions_learner_parts if part in ground_truth_parts]
        missing_parts = [part for part in ground_truth_parts if part not in solutions_learner_parts]

        if len(solutions_learner_parts) == len(ground_truth_parts) and not missing_parts:
            return 'Great! You found all complete extensions.'
        if len(overlapping_parts) < len(solutions_learner_parts):
            not_complete = ['{' + ', '.join(part) + '}'
                            for part in solutions_learner_parts if part not in ground_truth_parts]
            return 'The following parts of your answer were not complete extensions:\n' + '\n'.join(not_complete)
        return 'You missed the following complete extensions:\n' + '\n'.join(['{' + ', '.join(missing) + '}'
                                                                              for missing in missing_parts])
