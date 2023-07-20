from io import StringIO

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework


class ArgumentationFrameworkToICCMA23FormatWriter:
    @staticmethod
    def write_to_str(argumentation_framework: AbstractArgumentationFramework) -> str:
        arg_name_to_index_dict = \
            {name: str(index + 1) for index, name in enumerate([arg.name for arg in argumentation_framework.arguments])}

        sentence = StringIO()
        sentence.write('p af ' + str(len(argumentation_framework.arguments)) + '\n')
        for defeat in argumentation_framework.defeats:
            sentence.write(arg_name_to_index_dict[defeat.from_argument.name] + ' ' +
                           arg_name_to_index_dict[defeat.to_argument.name] + '\n')
        return sentence.getvalue()
