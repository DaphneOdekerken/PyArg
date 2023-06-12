from abc import ABC, abstractmethod
from typing import List

import dash_bootstrap_components as dbc
import visdcc

from src.py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data


class AbstractExerciseSet(ABC):
    @staticmethod
    def argumentation_framework_to_exercise_instance(argumentation_framework):
        return ', '.join(argument.name for argument in argumentation_framework.arguments) + ';' + \
            ', '.join('(' + defeat.from_argument.name + ', ' + defeat.to_argument.name + ')'
                      for defeat in argumentation_framework.defeats)

    @staticmethod
    def argumentation_framework_to_graph_data(argumentation_framework, color_blind_mode):
        return get_argumentation_framework_graph_data(argumentation_framework, None, color_blind_mode)

    @abstractmethod
    def get_explanation_html(self):
        pass

    @abstractmethod
    def generate_exercise_and_solutions(self, color_blind_mode: bool):
        pass

    @abstractmethod
    def render_exercise_instance_text(self, challenge_instance):
        pass

    @staticmethod
    def render_exercise_graph(graph_data):
        return visdcc.Network(data=graph_data, options={'height': '200px'},
                              id='exercise-graph')

    def render_exercise_instance(self, challenge_instance, graph_data):
        return dbc.Row([
            dbc.Col(self.render_exercise_instance_text(challenge_instance)),
            dbc.Col(self.render_exercise_graph(graph_data))
        ])

    @abstractmethod
    def get_feedback(self, solution_by_user: str, pre_generated_solutions: List[str]):
        pass
