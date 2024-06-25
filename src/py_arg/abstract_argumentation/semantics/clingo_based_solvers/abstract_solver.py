from typing import FrozenSet, Set

import clingo

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument


class AbstractSolver:
    def __init__(self):
        # Initialize clingo Control for enumerating all models.
        self.control = clingo.Control()
        self.control.configuration.solve.models = 0

        # Initialize variables for storing argumentation information.
        self.argumentation_framework = None
        self.argument_name_to_id = {}
        self.id_to_argument_name = {}
        self.all_extensions = set()

    def load_argumentation_framework(
            self, argumentation_framework: AbstractArgumentationFramework):
        self.argumentation_framework = argumentation_framework
        for arg_id, argument in enumerate(argumentation_framework.arguments):
            id_name = 'a' + str(arg_id)
            self.argument_name_to_id[argument.name] = id_name
            self.id_to_argument_name[id_name] = argument.name
            self.control.add('base', [], f'arg({id_name}).')
        for defeat in argumentation_framework.defeats:
            from_id = self.argument_name_to_id[defeat.from_argument.name]
            to_id = self.argument_name_to_id[defeat.to_argument.name]
            self.control.add('base', [], f'att({from_id},{to_id}).')

    def load_semantics_programs(self):
        pass

    def add_model_to_extension(self, model):
        new_extension = self.model_to_extension(model)
        self.all_extensions.add(new_extension)

    def model_to_extension(self, model) -> FrozenSet[Argument]:
        extension_elements = set()
        model_symbols = model.symbols(shown=True)
        for symbol in model_symbols:
            if symbol.name == 'in':
                argument_name = \
                    self.id_to_argument_name[symbol.arguments[0].name]
                in_argument = \
                    self.argumentation_framework.get_argument(argument_name)
                extension_elements.add(in_argument)
        return frozenset(extension_elements)

    def get_all_extensions(
            self, argumentation_framework: AbstractArgumentationFramework) -> \
            Set[FrozenSet[Argument]]:
        self.load_argumentation_framework(argumentation_framework)
        self.load_semantics_programs()
        self.control.ground([('base', [])])
        self.control.solve(on_model=self.add_model_to_extension)
        return self.all_extensions
