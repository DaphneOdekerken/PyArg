import json

from src.py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from src.py_arg.import_export.writer import Writer


class ArgumentationFrameworkToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def to_dict(argumentation_framework: AbstractArgumentationFramework):
        return {'name': argumentation_framework.name,
                'arguments': [str(argument) for argument in argumentation_framework.arguments],
                'defeats': [(str(defeat.from_argument), str(defeat.to_argument))
                            for defeat in argumentation_framework.defeats]}

    def write(self, argumentation_framework: AbstractArgumentationFramework, file_name: str):
        write_path = self.data_folder / file_name
        result = self.to_dict(argumentation_framework)
        with open(write_path, 'w') as write_file:
            json.dump(result, write_file)
