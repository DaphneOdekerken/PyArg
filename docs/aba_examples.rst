Using the ABA functionalities
=============================

In case you use the PyArg package ``python-argumentation``, we provide
below an example of some of its possibilities for Assumption-Based Argumentation (ABA).

The example below is Example 3.1 from:
Toni, Francesca. A tutorial on assumption-based argumentation. *Argument & Computation* 5.1 (2014): 89-117.

.. code:: python

    from py_arg.aba_classes.rule import Rule
    from py_arg.aba_classes.aba_framework import ABAF
    from py_arg.aba_classes.semantics import get_preferred_extensions


    language = {'happy',
                'eating',
                'good_food',
                'not_eating',
                'no_fork',
                'dirty_hands',
                'fork',
                'clean_hands'}
    rules = {Rule('Rule1', {'good_food', 'eating'}, 'happy'),
             Rule('Rule2', set(), 'good_food'),
             Rule('Rule3', {'no_fork', 'dirty_hands'}, 'not_eating')}
    assumptions = {'eating', 'no_fork', 'dirty_hands'}
    contraries = {'eating': 'not_eating',
                  'no_fork': 'fork',
                  'dirty_hands': 'clean_hands'}

    # Construct the framework
    aba_framework = ABAF(assumptions, rules, language, contraries)

    # Get preferred extensions
    extensions = get_preferred_extensions.apply(aba_framework)
    print(extensions)
