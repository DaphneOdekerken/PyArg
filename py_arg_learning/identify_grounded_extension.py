from typing import List

from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension
from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg_learning.abstract_exercise_set import AbstractExerciseSet


class IdentifyGroundedExtension(AbstractExerciseSet):
    def get_explanation_html(self):
        # TODO better explanation
        return "The grounded extension is the minimal complete extension w.r.t. set inclusion."

    def generate_exercise_and_solutions(self):
        argumentation_framework_generator = AbstractArgumentationFrameworkGenerator(5, 4, True)
        af = argumentation_framework_generator.generate()

        exercise_instance = self.argumentation_framework_to_exercise_instance(af)
        graph_data = self.argumentation_framework_to_graph_data(af)

        grounded_extension = sorted(get_grounded_extension(af))
        grounded_extension_argument_names = [argument.name for argument in grounded_extension]
        solution = ','.join(grounded_extension_argument_names)
        return exercise_instance, graph_data, [solution]

    def render_exercise_instance_text(self, exercise_instance):
        exercise_instance_parts = exercise_instance.split(';')
        exercise_text = 'Consider an abstract argumentation framework AF = (A, R) with A = {{{a}}} and R = {{{r}}}. ' \
                        'Which arguments belong to the grounded extension (divide by commas)?'.format(
                                a=exercise_instance_parts[0],
                                r=exercise_instance_parts[1])
        return exercise_text

    def get_feedback(self, solution_by_user: str, pre_generated_solutions: List[str]):
        def preprocess(input_str: str) -> List[str]:
            for c in '{}[]':
                input_str = input_str.replace(c, '')
            output_unsorted = [solution_part.strip() for solution_part in input_str.upper().split(',')]
            return sorted(output_unsorted)

        solution_learner = preprocess(solution_by_user)
        ground_truth = preprocess(pre_generated_solutions[0])
        if solution_learner == ground_truth:
            return 'Correct!'
        else:
            return 'This is not correct. The right answer was ' + pre_generated_solutions[0] + '.'
