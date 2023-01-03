from py_arg.aspic_classes.literal import Literal


class ConnectedLiteral(Literal):
    def __init__(self, literal_str: str):
        super().__init__(literal_str)
        self.init_connected_literal()

    def init_connected_literal(self):
        self.children = []
        self.parents = []
