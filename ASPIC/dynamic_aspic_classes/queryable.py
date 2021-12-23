from ASPIC.aspic_classes.literal import Literal


class Queryable(Literal):
    """
    A Queryable is a special case of a Literal which is observable and has a number of extra variables: a short and long
    query string and an observed boolean.
    """
    def __init__(self, literal_str: str,
                 description_if_present: str = '',
                 description_if_not_present: str = '',
                 query: str = '',
                 query_explanation: str = '',
                 priority: float = 0):
        super().__init__(literal_str, description_if_present, description_if_not_present)
        self.natural_language_query = query
        self.long_natural_language_query = query_explanation
        self.priority = priority
