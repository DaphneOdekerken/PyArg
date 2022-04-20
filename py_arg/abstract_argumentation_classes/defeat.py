from py_arg.abstract_argumentation_classes.argument import Argument


class Defeat:
    def __init__(self, from_argument: Argument, to_argument: Argument):
        self.from_argument = from_argument
        self.to_argument = to_argument

    def __str__(self):
        return str(self.from_argument) + ' defeats ' + str(self.to_argument)

    def __eq__(self, other):
        return self.from_argument == other.from_argument and self.to_argument == other.to_argument
