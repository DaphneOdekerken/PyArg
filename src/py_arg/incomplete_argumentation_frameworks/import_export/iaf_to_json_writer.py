import json

from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg.incomplete_aspic.import_export.writer import Writer


class IAFToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def to_dict(iaf: IncompleteArgumentationFramework):
        return {'name': iaf.name,
                'certain_arguments':
                    [str(argument)
                     for argument in iaf.arguments.values()],
                'uncertain_arguments':
                    [str(argument)
                     for argument in iaf.uncertain_arguments.values()],
                'certain_defeats': [(str(defeat.from_argument),
                                     str(defeat.to_argument))
                                    for defeat in iaf.defeats],
                'uncertain_defeats': [(str(defeat.from_argument),
                                       str(defeat.to_argument))
                                      for defeat in iaf.uncertain_defeats]
                }

    def write(self, iaf: IncompleteArgumentationFramework, file_name: str):
        write_path = self.data_folder / file_name
        result = self.to_dict(iaf)
        with open(write_path, 'w') as write_file:
            json.dump(result, write_file)
