from abc import ABC, abstractmethod
from typing import List


class AbstractExerciseSet(ABC):
    @abstractmethod
    def get_explanation_html(self):
        pass

    @abstractmethod
    def generate_exercise_and_solutions(self):
        pass

    @abstractmethod
    def render_exercise_instance(self, challenge_instance):
        pass

    @abstractmethod
    def get_feedback(self, solution_by_user: str, pre_generated_solutions: List[str]):
        pass
