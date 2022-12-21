from .literal import Literal


class Axiom(Literal):
    def __init__(self, literal_str: str, description_if_present: str, description_if_not_present: str):
        super().__init__(literal_str)
