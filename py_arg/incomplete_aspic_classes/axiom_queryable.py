from py_arg.incomplete_aspic_classes.queryable import Queryable


class AxiomQueryable(Queryable):
    def __init__(self, literal_str: str, description_if_present: str, description_if_not_present: str, query: str,
                 query_explanation: str, priority: float):
        super().__init__(literal_str, description_if_present, description_if_not_present, query, query_explanation,
                         priority)
