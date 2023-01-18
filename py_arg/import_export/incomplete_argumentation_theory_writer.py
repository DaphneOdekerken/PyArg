import pathlib

from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class IncompleteArgumentationTheoryWriter:
    def __init__(self):
        self.data_folder = pathlib.Path(__file__).parent.parent / 'experiments' / 'generated_data'
        if not self.data_folder.is_dir():
            self.data_folder.mkdir()

    def write(self, incomplete_argumentation_theory: IncompleteArgumentationTheory, write_path):
        pass
