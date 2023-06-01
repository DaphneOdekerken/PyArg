from typing import Optional

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


class ArgumentationFrameworkFromICCMA23FormatReader:
    @staticmethod
    def from_iccma23(iccma_23_str: str, argumentation_framework_name: Optional[str] = None) -> AbstractArgumentationFramework:
        if argumentation_framework_name:
            name = argumentation_framework_name
        else:
            name = ''

        lines = iccma_23_str.split('\n')
        nr_argument_lines = int(lines[0].split(' ')[2])
        arguments = [Argument('A' + str(index)) for index in range(1, nr_argument_lines + 1)]
        defeats = []
        for line in lines[1:]:
            if line:
                defeat_parts = line.split(' ')
                defeats.append(Defeat(Argument('A' + defeat_parts[0]),
                                      Argument('A' + defeat_parts[1])))
        return AbstractArgumentationFramework(name, arguments, defeats)
