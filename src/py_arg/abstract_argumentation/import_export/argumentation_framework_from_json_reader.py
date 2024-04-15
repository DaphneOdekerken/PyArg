import json

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


class ArgumentationFrameworkFromJsonReader:
    def __init__(self):
        pass

    @staticmethod
    def from_json(json_object) -> AbstractArgumentationFramework:
        if json_object['name']:
            name = json_object['name']
        else:
            name = ''
        arguments = [Argument(argument_name)
                     for argument_name in json_object['arguments']]
        defeats = [Defeat(Argument(from_argument), Argument(to_argument)) for
                   from_argument, to_argument in json_object['defeats']]
        return AbstractArgumentationFramework(name, arguments, defeats)

    def read_from_json(self, file_path: str) -> AbstractArgumentationFramework:
        with open(file_path, 'r') as reader:
            argumentation_framework_json = json.load(reader)
        return self.from_json(argumentation_framework_json)
