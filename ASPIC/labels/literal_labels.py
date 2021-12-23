from typing import Dict

from ASPIC.aspic_classes.literal import Literal
from ASPIC.labels.label import Label


class LiteralLabels:
    def __init__(self, literal_labeling: Dict[Literal, Label]):
        self.literal_labeling = literal_labeling

    def __getitem__(self, item):
        if not isinstance(item, Literal):
            raise ValueError(f'{item} is not a Literal!')
        return self.literal_labeling[item]
