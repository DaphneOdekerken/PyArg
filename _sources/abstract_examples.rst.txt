Using the abstract argumentation functionalities
================================================

Obtaining an abstract argumentation framework
---------------------------------------------
There are various ways to obtain an abstract argumentation framework (AF).
In this section, we discuss how AF's can be created from scratch, generated randomly or read from an existing file.

Creating an Argumentation Framework from scratch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First, we show how AF's can be created from scratch. This can be useful when experimenting with small AF's that are
not yet in an importable format.
Suppose we want to create an AF with three arguments A, B and C, where A and B defeat each other and B defeats C.
Then we can use the following code:

.. code:: python

    from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
    from py_arg.abstract_argumentation_classes.argument import Argument
    from py_arg.abstract_argumentation_classes.defeat import Defeat


    a = Argument('a')
    b = Argument('b')
    c = Argument('c')
    arguments = [a, b, c]
    defeats = [Defeat(a, b), Defeat(b, a), Defeat(b, c)]
    af = AbstractArgumentationFramework('af', arguments, defeats)

Generating an Argumentation Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Alternatively, we can randomly generate an AF with, for example, three arguments and three defeats.

.. code:: python

    from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator


    generator = AbstractArgumentationFrameworkGenerator(3, 3, True)
    af = generator.generate()

Reading an Argumentation Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Another option is to read the argumentation framework from a str, possibly obtained from a file.
PyArg provides various readers. Below we give an example for the ASPARTIX format reader:

.. code:: python

    from py_arg.import_export.argumentation_framework_from_aspartix_format_reader import \
    ArgumentationFrameworkFromASPARTIXFormatReader


    test_file_str = 'arg(A).\n' \
                    'arg(B).\n' \
                    'arg(C).\n' \
                    'att(A, B).\n' \
                    'att(B, C).\n' \
                    'att(B, A).\n'
    af = ArgumentationFrameworkFromASPARTIXFormatReader.from_apx(test_file_str)

Applying algorithms
-------------------
Given an abstract argumentation framework, we can apply various algorithms to it.
These can be found in the algorithms folder.
Next, we give an example of obtaining the complete extensions of a given AF:

.. code:: python

    from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
    from py_arg.abstract_argumentation_classes.argument import Argument
    from py_arg.abstract_argumentation_classes.defeat import Defeat
    from py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions


    b = Argument('b')
    c = Argument('c')
    d = Argument('d')
    arguments = [b, c, d]
    defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
    af = AbstractArgumentationFramework('af', arguments, defeats)
    ces = get_complete_extensions(af)
