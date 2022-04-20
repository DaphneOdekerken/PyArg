from typing import List, Literal

from py_arg.dynamic_aspic_classes.potential_argument import PotentialArgument
from py_arg.dynamic_aspic_classes.queryable import Queryable


def get_relevant_literals_for_potential_argument(potential_argument: PotentialArgument,
                                                 knowledge_base: List[Queryable]) -> List[Literal]:
    return [queryable for queryable in potential_argument.premises
            if queryable not in knowledge_base]
