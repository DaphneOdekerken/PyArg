Using the ASPIC+ functionalities
================================

In case you use the PyArg package ``python-argumentation``, we provide
below an example of some of its possibilities.

Creating an ASPIC+ argumentation theory from scratch
----------------------------------------------------

The example below is taken from S.J. Modgil & H. Prakken, A general
account of argumentation with preferences. *Artificial Intelligence* 195
(2013): 361-397.

.. code:: python

   from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
   from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
   from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
   from py_arg.aspic_classes.literal import Literal
   from py_arg.aspic_classes.strict_rule import StrictRule


   def get_argumentation_theory():
       # Language
       literal_str_list = ['a', 'p', 'q', 'r', 's', 't']
       literal_str_list += ['-' + literal_str for literal_str in literal_str_list]
       literal_str_list += ['~' + literal_str for literal_str in literal_str_list]
       language = {literal_str: Literal(literal_str)
                   for literal_str in literal_str_list}

       # Contradiction function
       contraries_and_contradictories = {literal_str: [] for literal_str in language.keys()}
       for literal_str in language.keys():
           if literal_str[0] in ('~', '-'):
               contraries_and_contradictories[literal_str].append(language[literal_str[1:]])
           else:
               contraries_and_contradictories[literal_str].append(language['-' + literal_str])

       # Strict rules
       strict_rules = [StrictRule('s1', {language['t'], language['q']}, language['-p'])]

       # Defeasible rules
       d1 = DefeasibleRule('d1', {language['~s']}, language['t'])
       d2 = DefeasibleRule('d2', {language['r']}, language['q'])
       d3 = DefeasibleRule('d3', {language['a']}, language['p'])
       defeasible_rules = [d1, d2, d3]

       # n (naming from defeasible rules to literals) and updating the contradiction function
       for defeasible_rule in defeasible_rules:
           defeasible_rule_literal = Literal.from_defeasible_rule(defeasible_rule)
           defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(defeasible_rule)
           language[str(defeasible_rule_literal)] = defeasible_rule_literal
           language[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation
           contraries_and_contradictories[str(defeasible_rule_literal)] = [defeasible_rule_literal_negation]
           contraries_and_contradictories[str(defeasible_rule_literal_negation)] = [defeasible_rule_literal]

       # Argumentation system
       arg_sys = ArgumentationSystem(language, contraries_and_contradictories, strict_rules, defeasible_rules)

       # Knowledge base
       axioms = []
       ordinary_premises = [language[literal_str] for literal_str in ['a', 'r', '-r', '~s']]

       # Argumentation theory
       arg_theory = ArgumentationTheory(arg_sys, axioms, ordinary_premises)
       return arg_theory

Printing all arguments and their properties
-------------------------------------------

.. code:: python

   argumentation_theory = get_argumentation_theory()

   for argument in argumentation_theory.all_arguments:
       print('The argument is: ' + str(argument))
       print('Conclusion: ' + str(argument.conclusion))
       print('Premises: {' + ', '.join(str(premise) for premise in argument.premises) + '}')
       print('Strict rules: {' + ', '.join(str(rule) for rule in argument.strict_rules) + '}')
       print('Defeasible rules: {' + ', '.join(str(rule) for rule in argument.defeasible_rules) + '}')
       print('Top rule: ' + str(argument.top_rule))
       print()

Printing all attacks
--------------------

.. code:: python

   argumentation_theory = get_argumentation_theory()

   # All attacks, independent of type
   for attack in argumentation_theory.all_attacks:
       print(attack)

Printing specific attacks
-------------------------

.. code:: python

   argumentation_theory = get_argumentation_theory()

   # All undercutters
   all_underminers = [(argument_a, argument_b)
       for argument_a in argumentation_theory.all_arguments
       for argument_b in argumentation_theory.all_arguments
       if argumentation_theory.undermines(argument_a, argument_b)]
   print('*Underminers:*')
   for attack in all_underminers:
       print(attack)

Creating an abstract argumentation framework
--------------------------------------------

Note: if no specific ordering is given, last link elitist ordering is
chosen as default ordering

.. code:: python

   arg_theory = get_argumentation_theory()
   af = arg_theory.create_abstract_argumentation_framework('af')

   arg_for_r = af.get_argument('r (ordinary premise)')
   defeaters_of_r = arg_for_r.get_ingoing_defeat_arguments
   print('*Defeaters of the argument for r*')
   for defeater in defeaters_of_r:
       print(defeater)
   print()

   arg_for_not_r = af.get_argument('-r (ordinary premise)')
   defeated_by_not_r = arg_for_not_r.get_outgoing_defeat_arguments
   print('*Arguments defeated by the argument for not r*')
   for defeated in defeated_by_not_r:
       print(defeated)
   print()

Finding extensions
------------------

.. code:: python

   from py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions
   from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension


   grounded_extension = get_grounded_extension(af)
   print('*Grounded extension:*')
   print('{' + ', '.join(str(grounded) for grounded in grounded_extension) + '}')
   print()

   complete_extensions = get_complete_extensions(af)
   print('*Complete extensions:*')
   for complete_extension in complete_extensions:
       print('{' + ', '.join(str(complete) for complete in complete_extension) + '}')
   print()