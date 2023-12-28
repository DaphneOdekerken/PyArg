from py_arg.abstract_argumentation.explanation.get_defending_arguments \
    import get_defending_arguments_in_extensions, \
    get_directly_defending_arguments
from py_arg.abstract_argumentation.explanation.get_attackers_without_defense \
    import get_attackers_without_defense_in_extensions, get_no_dir_defending, \
    get_no_self_defense
from py_arg.abstract_argumentation.explanation.suff_nec \
    import get_sufficient_or_necessary


def get_str_explanations(argumentation_theory, semantics,
                         ordering_specification, extensions, accepted_formulas,
                         function, expl_type, strategy, form):
    """
    Calculate, for each formula, the explanations, given the function, type,
    strategy and form.

    :param argumentation_theory: the argumentation theory the explanation has
    to be calculated from.
    :param semantics: The semantics used to determine (non-)acceptance.
    :param ordering_specification: The chosen ordering, combining both
    last/weakest link and democratic/elitist.
    :param extensions: The sets of accepted arguments in arg_framework,
    based on semantics.
    :param accepted_formulas: The formulas that are considered accepted
    given the extensions and strategy.
    :param function: The explanation function, to determine the content
    of the explanation.
    :param expl_type: The explanation type, to determine
    acceptance/non-acceptance explanation.
    :param strategy: The strategy of the explanation, whether credulous
    or skeptical reasoning.
    :param form: The form of the explanation, for example, explanations
    in terms of arguments, rules or premises.
    :return: A dictionary with for each (non-)accepted argument its
    explanation, given the parameters.
    """
    argumentation_framework = \
        argumentation_theory.create_abstract_argumentation_framework(
            'af', ordering_specification)
    abstract_explanation = {}
    if expl_type == 'Acceptance':
        for formula in accepted_formulas:
            form_arg = argumentation_theory.arguments[formula]
            arg_expl = []
            suff_expl = []
            for arg in form_arg:
                if function == 'Defending':
                    arg_expl.extend(get_defending_arguments_in_extensions(
                        argumentation_framework, arg, extensions))
                elif function == 'DirDefending':
                    arg_expl.extend(get_directly_defending_arguments(
                        argumentation_framework, arg, extensions))
                else:
                    suff_expl.extend(get_sufficient_or_necessary(
                        argumentation_framework, arg, 'Suff', expl_type))
            if suff_expl != []:
                if function == 'Suff':
                    arg_expl.extend(suff_expl)
                else:
                    form_expl = []
                    form_expls = []
                    if form == 'Arg':
                        form_expl = suff_expl
                    else:
                        for sets in suff_expl:
                            set_expl = []
                            for arg in sets:
                                if form == 'Prem' and \
                                        arg.premises not in form_expl:
                                    set_expl.append(arg.premises)
                                elif form == 'Rule':
                                    defrules = arg.defeasible_rules
                                    rules = defrules.union(arg.strict_rules)
                                    if rules not in form_expl:
                                        set_expl.append(rules)
                                elif form == 'SubArg' \
                                        and arg.sub_arguments not in form_expl:
                                    set_expl.append(arg.sub_arguments)
                                elif form == 'SubArgConclusions':
                                    subargconc = set()
                                    for subarg in arg.sub_arguments:
                                        if subarg.conclusion not in subargconc:
                                            subargconc.add(subarg.conclusion)
                                    set_expl.append(subargconc)
                            form_expl.append(set_expl)

                        for expl in form_expl:
                            form_expls.append(set().union(*expl))
                        form_expl = form_expls

                    if function == 'MinSuff':
                        minsuff_expl = []
                        sort_form_expl = sorted(form_expl, key=len)
                        for suff in sort_form_expl:
                            minsuff_suff = []
                            for minsuff in minsuff_expl:
                                if minsuff.issubset(suff):
                                    minsuff_suff.append(minsuff)
                                if suff.issubset(minsuff):
                                    minsuff_expl.remove(minsuff)
                                    minsuff_suff.append(suff)
                            if minsuff_suff == [] and suff not in minsuff_expl:
                                minsuff_expl.append(suff)
                        arg_expl.extend(minsuff_expl)

                    elif function == 'Nec':
                        nec_expl = form_expl[0]
                        for suffexpl in form_expl:
                            nec_expl = nec_expl.intersection(suffexpl)
                        arg_expl.extend(nec_expl)
#
            abstract_explanation[str(formula)] = arg_expl

        if function == 'MinSuff' or function == 'Nec':
            return abstract_explanation

    elif expl_type == 'NonAcceptance':
        formulas = set()
        for arg in argumentation_framework.arguments:
            for subarg in arg.sub_arguments:
                formulas.add(subarg.conclusion)
        for formula in formulas.difference(accepted_formulas):
            form_arg = argumentation_theory.arguments[formula]
            arg_expl = []
            for arg in form_arg:
                if function == 'NoDefAgainst':
                    arg_expl.extend(
                        get_attackers_without_defense_in_extensions(
                            argumentation_framework, arg, extensions))
                elif function == 'NoDirDefense':
                    arg_expl.extend(get_no_dir_defending(
                        argumentation_framework, arg, extensions))
                elif function == 'NoSelfDefense':
                    arg_expl.extend(get_no_self_defense(
                        argumentation_framework, arg, extensions))
            abstract_explanation[str(formula)] = arg_expl

    if form == 'Arg':
        return abstract_explanation
    else:
        for expl_form in abstract_explanation:
            explanation = abstract_explanation[expl_form]
            form_expl = []
            for sets in explanation:
                for arg in sets:
                    if form == 'Prem' and arg.premises not in form_expl:
                        form_expl.append(arg.premises)
                    elif form == 'Rule':
                        defrules = arg.defeasible_rules
                        rules = defrules.union(arg.strict_rules)
                        if rules not in form_expl:
                            form_expl.append(rules)
#                    elif form == 'TopRule':
#                        if arg.top_rule != None:
#                            if arg.top_rule not in form_expl:
#                                form_expl.append(arg.top_rule)
                    elif form == 'SubArg' and \
                            arg.sub_arguments not in form_expl:
                        form_expl.append(arg.sub_arguments)
                    elif form == 'SubArgConclusions':
                        subargconc = set()
                        for subarg in arg.sub_arguments:
                            if subarg.conclusion not in subargconc:
                                subargconc.add(subarg.conclusion)
                        form_expl.append(subargconc)
            abstract_explanation[expl_form] = form_expl
        return abstract_explanation
