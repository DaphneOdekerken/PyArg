from typing import Optional, List, Tuple

from py_arg.abstract_argumentation_classes.argument import Argument


class StructuredArgumentationFramework:
    def __init__(self, name: str = '',
                 arguments: Optional[List[Argument]] = None,
                 attacks: Optional[List[Tuple[Argument, Argument]]] = None,
                 argument_preference_relation: Optional[List[Tuple[Argument, Argument]]] = None):
        self.name = name

        if arguments is None:
            self._arguments = {}
        else:
            self._arguments = {argument.name: argument for argument in arguments}

        if attacks is None:
            self.attacks = []
        else:
            self.attacks = attacks

        if argument_preference_relation is None:
            self.argument_preference_relation = [(argument, argument) for argument in self._arguments.values()]
        else:
            self.argument_preference_relation = argument_preference_relation
