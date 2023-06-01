from typing import Optional

import parse

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


class ArgumentationFrameworkFromASPARTIXFormatReader:
    @staticmethod
    def from_apx(apx_str: str, argumentation_framework_name: Optional[str] = None) -> AbstractArgumentationFramework:
        if argumentation_framework_name:
            name = argumentation_framework_name
        else:
            name = ''

        argument_strs = [r[0] for r in parse.findall('arg({}).', apx_str)]
        defeat_strs = [(r[0], r[1]) for r in parse.findall('att({},{}).', apx_str)]

        arguments = [Argument(arg_str) for arg_str in argument_strs]
        defeats = [Defeat(Argument(defeat_str[0]), Argument(defeat_str[1]))
                   for defeat_str in defeat_strs]
        return AbstractArgumentationFramework(name, arguments, defeats)
