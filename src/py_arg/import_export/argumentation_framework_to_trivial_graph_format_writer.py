from io import StringIO

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework


class ArgumentationFrameworkToTrivialGraphFormatWriter:
    @staticmethod
    def write_to_str(argumentation_framework: AbstractArgumentationFramework) -> str:
        sentence = StringIO()
        for argument in argumentation_framework.arguments:
            sentence.write(argument.name + '\n')
        sentence.write('#\n')
        for defeat in argumentation_framework.defeats:
            sentence.write(defeat.from_argument.name + ' ' + defeat.to_argument.name + '\n')
        return sentence.getvalue()
