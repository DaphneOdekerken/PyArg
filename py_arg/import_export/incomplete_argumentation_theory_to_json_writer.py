from py_arg.import_export.incomplete_argumentation_theory_writer import Writer
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class IncompleteArgumentationTheoryToJSONWriter(Writer):
    def __init__(self):
        super().__init__()

    def write(self, incomplete_argumentation_theory: IncompleteArgumentationTheory, file_name: str):
        write_path = self.data_folder / file_name
        # TODO
