from enum import Enum
from typing import Set, Dict, FrozenSet

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


# Algorithm 1 from Nofal, Samer, Katie Atkinson, and Paul E. Dunne. "Algorithms for decision problems in argument
# systems under preferred semantics." Artificial Intelligence 207 (2014): 23-51.


class PreferredExtensionLabel(Enum):
    IN = 1              # Arguments *might* be in a preferred extension
    OUT = 2             # Argument is defeated by an IN argument
    BLANK = 3           # Default label for all arguments, indicating that the argument is still unprocessed.
    MUST_OUT = 4        # Argument defeats IN argument
    UNDEC = 5           # Argument may not be included in a preferred extension because not defended by any IN argument.


def get_preferred_extensions(argumentation_framework: AbstractArgumentationFramework) -> Set[FrozenSet[Argument]]:
    """
    Get the preferred extensions of an argumentation framework.

    :param argumentation_framework: The argumentation framework for which we need the preferred extensions.
    :return: Preferred extension of the argumentation framework.

    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [b, c, d]
    >>> defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
    >>> pes = get_preferred_extensions(af)
    >>> len(pes)
    1
    >>> frozenset({b, d}) in pes
    True
    >>> frozenset({b}) in pes
    False
    """
    initial_labelling = {argument: PreferredExtensionLabel.BLANK
                         for argument in argumentation_framework.arguments}
    return _recursively_get_preferred_extensions(argumentation_framework, initial_labelling, set())


def _recursively_get_preferred_extensions(argumentation_framework: AbstractArgumentationFramework,
                                          labelling: Dict[Argument, PreferredExtensionLabel],
                                          preferred_extensions: Set[FrozenSet[Argument]]) -> Set[FrozenSet[Argument]]:
    if all(labelling[argument] != PreferredExtensionLabel.BLANK for argument in argumentation_framework.arguments):
        if all(labelling[argument] != PreferredExtensionLabel.MUST_OUT
               for argument in argumentation_framework.arguments):
            candidate_preferred_extension = frozenset(sorted({argument for argument in argumentation_framework.arguments
                                                              if labelling[argument] == PreferredExtensionLabel.IN}))
            if not any(candidate_preferred_extension < preferred_extension
                       for preferred_extension in preferred_extensions):
                preferred_extensions.add(candidate_preferred_extension)
    else:
        blank_argument = [argument for argument in argumentation_framework.arguments
                          if labelling[argument] == PreferredExtensionLabel.BLANK][0]
        alternative_labelling = _in_trans(labelling, blank_argument, argumentation_framework)
        preferred_extensions = _recursively_get_preferred_extensions(argumentation_framework, alternative_labelling,
                                                                     preferred_extensions)
        alternative_labelling = _undec_trans(labelling, blank_argument)
        preferred_extensions = _recursively_get_preferred_extensions(argumentation_framework, alternative_labelling,
                                                                     preferred_extensions)
    return preferred_extensions


def _in_trans(labelling: Dict[Argument, PreferredExtensionLabel], argument: Argument,
              argumentation_framework: AbstractArgumentationFramework) -> Dict[Argument, PreferredExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = PreferredExtensionLabel.IN
    for defeater in argumentation_framework.get_outgoing_defeat_arguments(argument):
        if defeater == argument: break
        else:
            new_labelling[defeater] = PreferredExtensionLabel.OUT
    for defeated in argumentation_framework.get_incoming_defeat_arguments(argument):
        if new_labelling[defeated] != PreferredExtensionLabel.OUT:
            new_labelling[defeated] = PreferredExtensionLabel.MUST_OUT
    return new_labelling


def _undec_trans(labelling: Dict[Argument, PreferredExtensionLabel], argument: Argument) -> \
        Dict[Argument, PreferredExtensionLabel]:
    new_labelling = labelling.copy()
    new_labelling[argument] = PreferredExtensionLabel.UNDEC
    return new_labelling


if __name__ == "__main__":
    import doctest

    doctest.testmod()
