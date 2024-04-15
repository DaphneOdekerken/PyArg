from typing import Optional

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat


class ArgumentationFrameworkFromTrivialGraphFormatReader:
    @staticmethod
    def from_tgf(tgf_str: str,
                 argumentation_framework_name: Optional[str] = None) -> \
            AbstractArgumentationFramework:
        if argumentation_framework_name:
            name = argumentation_framework_name
        else:
            name = ''

        arguments = []
        defeats = []

        lines = tgf_str.split('\n')
        hashtag_seen = False
        for line in lines:
            if line == '#':
                hashtag_seen = True
            else:
                if not hashtag_seen:
                    arguments.append(Argument(line))
                else:
                    if line:
                        defeat_parts = line.split(' ')
                        defeats.append(Defeat(Argument(defeat_parts[0]),
                                              Argument(defeat_parts[1])))
        return AbstractArgumentationFramework(name, arguments, defeats)
