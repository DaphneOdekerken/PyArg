import json

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework


class IAFFromJsonReader:
    def __init__(self):
        pass

    @staticmethod
    def from_json(json_object) -> IncompleteArgumentationFramework:
        if json_object['name']:
            name = json_object['name']
        else:
            name = ''
        arguments = [Argument(argument_name)
                     for argument_name in json_object['certain_arguments']]
        uncertain_arguments = \
            [Argument(argument_name)
             for argument_name in json_object['uncertain_arguments']]
        defeats = [Defeat(Argument(from_arg), Argument(to_arg))
                   for from_arg, to_arg in json_object['certain_defeats']]
        uncertain_defeats = \
            [Defeat(Argument(from_arg), Argument(to_arg))
             for from_arg, to_arg in json_object['uncertain_defeats']]
        return IncompleteArgumentationFramework(
            name, arguments, uncertain_arguments, defeats, uncertain_defeats)

    def read_from_json(self, file_path: str) -> \
            IncompleteArgumentationFramework:
        with open(file_path, 'r') as reader:
            iaf_json = json.load(reader)
        return self.from_json(iaf_json)
