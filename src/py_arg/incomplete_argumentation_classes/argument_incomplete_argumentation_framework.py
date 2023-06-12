from typing import Optional, List, Dict

from src.py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from src.py_arg.abstract_argumentation_classes.argument import Argument
from src.py_arg.abstract_argumentation_classes.defeat import Defeat


class ArgumentIncompleteArgumentationFramework:
    # TODO: Docstrings and tests.

    def __init__(self, name: str = '',
                 arguments: Optional[List[Argument]] = None,
                 uncertain_arguments: Optional[List[Argument]] = None,
                 defeats: Optional[List[Defeat]] = None,
                 uncertain_defeats: Optional[List[Defeat]] = None):
        self.name = name

        if arguments is None:
            self._arguments = {}
        else:
            self._arguments = {argument.name: argument for argument in arguments}

        if uncertain_arguments is None:
            self._uncertain_arguments = {}
        else:
            if any(uncertain_argument in arguments for uncertain_argument in uncertain_arguments):
                raise ValueError('Argument cannot be both certain and uncertain.')
            self._uncertain_arguments = {argument.name: argument for argument in uncertain_arguments}

        if defeats is None:
            self._defeats = []
        else:
            self._defeats = defeats

        if uncertain_defeats is None:
            self._uncertain_defeats = []
        else:
            self._uncertain_defeats = defeats

        for defeat in self._defeats + self._uncertain_defeats:
            if defeat.from_argument.name in self._arguments.keys():
                defeat_from_argument = self._arguments[defeat.from_argument.name]
            else:
                defeat_from_argument = self._uncertain_arguments[defeat.from_argument.name]
            if defeat.to_argument.name in self._arguments.keys():
                defeat_to_argument = self._arguments[defeat.to_argument.name]
            else:
                defeat_to_argument = self._uncertain_arguments[defeat.to_argument.name]
            defeat_from_argument.add_outgoing_defeat(defeat.to_argument)
            defeat_to_argument.add_ingoing_defeat(defeat.from_argument)

    @property
    def arguments(self) -> Dict[str, Argument]:
        return self._arguments

    @property
    def uncertain_arguments(self) -> Dict[str, Argument]:
        return self._uncertain_arguments

    @property
    def certain_projection(self) -> AbstractArgumentationFramework:
        arguments = list(self._arguments.values())
        return AbstractArgumentationFramework(arguments=arguments,
                                              defeats=[defeat for defeat in self._defeats
                                                       if defeat.to_argument in arguments and
                                                       defeat.to_argument in arguments])

    def _get_direct_specifications(self):
        if self._uncertain_arguments:
            first_uncertain_argument = sorted(self._uncertain_arguments.keys())[0]
            new_uncertain_arguments = [value for key, value in self._uncertain_arguments.items()
                                       if key != first_uncertain_argument]
            return [
                ArgumentIncompleteArgumentationFramework(
                    arguments=list(self.arguments.values()),  uncertain_arguments=new_uncertain_arguments,
                    defeats=self._defeats, uncertain_defeats=self._uncertain_defeats),
                ArgumentIncompleteArgumentationFramework(
                    arguments=list(self.arguments.values()) + [self.arguments[first_uncertain_argument]],
                    uncertain_arguments=new_uncertain_arguments,
                    defeats=self._defeats, uncertain_defeats=self._uncertain_defeats),
            ]
        elif self._uncertain_defeats:
            first_uncertain_defeat = self._defeats[0]
            new_uncertain_defeats = self._defeats[1:]
            return [
                ArgumentIncompleteArgumentationFramework(
                    arguments=list(self.arguments.values()),
                    uncertain_arguments=list(self.uncertain_arguments.values()),
                    defeats=self._defeats, uncertain_defeats=new_uncertain_defeats
                ),
                ArgumentIncompleteArgumentationFramework(
                    arguments=list(self.arguments.values()),
                    uncertain_arguments=list(self.uncertain_arguments.values()),
                    defeats=self._defeats + [first_uncertain_defeat], uncertain_defeats=new_uncertain_defeats
                )
            ]
