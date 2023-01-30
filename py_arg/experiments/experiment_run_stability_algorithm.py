import pathlib
from typing import Tuple

from py_arg.algorithms.stability.stability_labeler import StabilityLabeler
from py_arg.algorithms.stability.stability_labels import StabilityLabels
from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.import_export.incomplete_argumentation_theory_from_lp_file_reader import \
    IncompleteArgumentationTheoryFromLPFileReader


def _run_stability_approximation_algorithm(lp_file_name: str) -> Tuple[StabilityLabels, ArgumentationSystem]:
    iat_lp_reader = IncompleteArgumentationTheoryFromLPFileReader()
    iat = iat_lp_reader.read_from_lp_file(str(pathlib.Path('generated_data') / lp_file_name))
    stability_labeler = StabilityLabeler()
    return stability_labeler.label(iat), iat.argumentation_system


def get_literal_is_stable(lp_file_name: str, literal_str: str):
    stability_labels, arg_sys = _run_stability_approximation_algorithm(lp_file_name)
    if stability_labels.literal_labeling[arg_sys.language[literal_str]].is_stable:
        print('YES')
    else:
        print('NO')


def get_literal_stability(lp_file_name: str, literal_str: str):
    stability_labels, arg_sys = _run_stability_approximation_algorithm(lp_file_name)
    print(stability_labels.literal_labeling[arg_sys.language[literal_str]].stability_str)


def get_all_literals_is_stable(lp_file_name: str):
    stability_labels, arg_sys = _run_stability_approximation_algorithm(lp_file_name)
    for literal in arg_sys.language.values():
        if stability_labels.literal_labeling[literal].is_stable:
            print(literal.s1 + ' ' + 'YES')
        else:
            print(literal.s1 + ' ' + 'NO')


def get_all_literals_stability(lp_file_name: str):
    stability_labels, arg_sys = _run_stability_approximation_algorithm(lp_file_name)
    for literal in arg_sys.language.values():
        print(literal.s1 + ' ' + stability_labels.literal_labeling[literal].stability_str)


if __name__ == "__main__":
    get_literal_is_stable('generated_iat.lp', 'l0')
    get_all_literals_stability('generated_iat.lp')
