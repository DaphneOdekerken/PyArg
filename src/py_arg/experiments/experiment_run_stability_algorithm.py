import os
import pathlib
from typing import Tuple

import datetime

from py_arg.algorithms.stability.stability_labeler import StabilityLabeler
from py_arg.algorithms.stability.stability_labels import StabilityLabels
from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.import_export.incomplete_argumentation_theory_from_lp_file_reader import \
    IncompleteArgumentationTheoryFromLPFileReader


def _run_stability_approximation_algorithm(lp_file_name: str) -> \
        Tuple[Tuple[StabilityLabels, ArgumentationSystem], Tuple[datetime,
        datetime, datetime]]:
    start_time = datetime.datetime.now()
    iat_lp_reader = IncompleteArgumentationTheoryFromLPFileReader()
    iat = iat_lp_reader.read_from_lp_file(
        str(pathlib.Path('generated_data') / lp_file_name))
    stability_labeler = StabilityLabeler()
    algorithm_start_time = datetime.datetime.now()
    result = stability_labeler.label(iat), iat.argumentation_system
    algorithm_end_time = datetime.datetime.now()
    return result, (start_time, algorithm_start_time, algorithm_end_time)


# def get_literal_is_stable(lp_file_name: str, literal_str: str):
#     stability_labels, arg_sys = _run_stability_approximation_algorithm(
#         lp_file_name)
#     if stability_labels.literal_labeling[arg_sys.language[
#             literal_str]].is_stable:
#         print('YES')
#     else:
#         print('NO')
#
#
# def get_literal_stability(lp_file_name: str, literal_str: str):
#     stability_labels, arg_sys = _run_stability_approximation_algorithm(
#         lp_file_name)
#     print(stability_labels.literal_labeling[arg_sys.language[
#         literal_str]].stability_str)
#
#
# def get_all_literals_is_stable(lp_file_name: str):
#     stability_labels, arg_sys = _run_stability_approximation_algorithm(
#         lp_file_name)
#     for literal in arg_sys.language.values():
#         if stability_labels.literal_labeling[literal].is_stable:
#             print(literal.s1 + ' ' + 'YES')
#         else:
#             print(literal.s1 + ' ' + 'NO')


def get_all_literals_stability(lp_file_name: str):
    (stability_labels, arg_sys), (start_time, alg_start_time, end_time) = \
        _run_stability_approximation_algorithm(lp_file_name)
    for literal in arg_sys.language.values():
        print(literal.s1 + ' ' + stability_labels.literal_labeling[
            literal].stability_str)
    return start_time, alg_start_time, end_time


if __name__ == "__main__":
    with os.scandir(r'generated_data') as entries:
        for entry in entries:
            filename = entry.name
            st, st2, et = get_all_literals_stability(filename)
            with open('results.csv', 'a') as writer:
                print(filename + ' ' +
                      str((et - st).total_seconds() * 1000) + ' ' +
                      str((et - st2).total_seconds() * 1000))
                writer.write(filename + ';' +
                             str((et - st).total_seconds() * 1000).replace(
                                 '.', ',') + ';' +
                             str((et - st2).total_seconds() * 1000).replace(
                                 '.', ',') + '\n')
