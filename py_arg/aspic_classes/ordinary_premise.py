from .literal import Literal


class OrdinaryPremise(Literal):
    def __init__(self, literal_str: str):
        super().__init__(literal_str)
