from enum import Enum


class EnumStabilityLabel(Enum):
    UNSATISFIABLE = 1
    DEFENDED = 2
    OUT = 3
    BLOCKED = 4
    UNSTABLE = 5
