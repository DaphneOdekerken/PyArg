from io import StringIO

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


class ArgumentationFrameworkToASPARTIXFormatWriter:
    @staticmethod
    def write_to_str(
            argumentation_framework: AbstractArgumentationFramework) -> str:
        sentence = StringIO()
        for argument in argumentation_framework.arguments:
            sentence.write('arg(' + argument.name + ').\n')
        for defeat in argumentation_framework.defeats:
            sentence.write('att(' + defeat.from_argument.name + ',' +
                           defeat.to_argument.name + ').\n')
        return sentence.getvalue()
