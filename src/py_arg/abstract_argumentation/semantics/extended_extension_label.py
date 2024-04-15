from enum import Enum


class ExtendedExtensionLabel(Enum):
    # Arguments *might* be in a preferred extension
    IN = 1
    # Argument is defeated by an IN argument
    OUT = 2
    # Default label for all arguments, indicating that the argument is still
    # unprocessed.
    BLANK = 3
    # Argument defeats some IN argument
    MUST_OUT = 4
    # Argument may not be included in a preferred extension because it is not
    # defended by any IN argument.
    UNDEC = 5
