from typing import Dict

from py_arg.incomplete_aspic_classes.potential_argument import PotentialArgument
from py_arg.labels.potential_argument_label import PotentialArgumentLabel


class PotentialArgumentLabels:
    def __init__(self, potential_argument_labeling: Dict[PotentialArgument, PotentialArgumentLabel]):
        self.potential_argument_labeling = potential_argument_labeling

    def __getitem__(self, item):
        if not isinstance(item, PotentialArgument):
            raise ValueError(f'{item} is not a PotentialArgument!')
        return self.potential_argument_labeling[item]

    def __setitem__(self, key, value):
        if not isinstance(key, PotentialArgument):
            raise ValueError(f'{key} is not a PotentialArgument!')
        if not isinstance(value, PotentialArgumentLabel):
            raise ValueError(f'{value} is not a PotentialArgumentLabel!')
        if key not in self.potential_argument_labeling.keys():
            raise ValueError(f'{key} is not recognised as a PotentialArgument.')
        self.potential_argument_labeling[key] = value
