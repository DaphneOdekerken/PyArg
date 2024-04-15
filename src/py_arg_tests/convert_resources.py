import pathlib

from py_arg.aspic.import_export.argumentation_system_to_json_writer \
    import ArgumentationSystemToJSONWriter
from py_arg.incomplete_aspic.import_export.\
    incomplete_argumentation_theory_from_xlsx_reader import \
    IncompleteArgumentationTheoryFromXLSXFileReader


def path_to_resources(filename: str):
    return pathlib.Path.cwd() / 'resources' / (filename + '.xlsx')


def convert_resources(filename: str):
    iatr = IncompleteArgumentationTheoryFromXLSXFileReader()
    arw = ArgumentationSystemToJSONWriter()
    iat = iatr.read_from_xlsx_file(path_to_resources(filename))
    arg_sys = iat.argumentation_system
    arw.write(arg_sys, filename + '.json')


def convert_all_xlsx_to_json():
    resource_folder = pathlib.Path.cwd() / 'resources'
    for file in resource_folder.iterdir():
        if file.is_file() and file.suffix == '.xlsx':
            try:
                convert_resources(file.stem)
            except ImportError:
                pass


convert_all_xlsx_to_json()
