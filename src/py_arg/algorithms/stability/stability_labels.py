from typing import Dict

from py_arg.algorithms.stability.stability_label import StabilityLabel
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.rule import Rule


class StabilityLabels:
    def __init__(self, literal_labeling: Dict[Literal, StabilityLabel], rule_labeling: Dict[Rule, StabilityLabel]):
        self.literal_labeling = literal_labeling
        self.rule_labeling = rule_labeling
