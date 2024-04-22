import pathlib
from typing import Set, FrozenSet, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.clingo_based_solvers.\
    abstract_solver import AbstractSolver


PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'
T = TypeVar('T', bound=Argument)


class GroundedSolver(AbstractSolver):
    def load_semantics_programs(self):
        self.control.load(str(PATH_TO_ENCODINGS / 'grounded.dl'))


def get_grounded_extension(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[T]:
    return set(get_grounded_extensions(argumentation_framework).pop())


def get_grounded_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[FrozenSet[T]]:
    solver = GroundedSolver()
    return solver.get_all_extensions(argumentation_framework)
