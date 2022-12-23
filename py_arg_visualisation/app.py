import dash
from dash import html
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate

import dash.dependencies

from py_arg_visualisation.functions.explanations_functions.get_af_explanations import get_argumentation_framework_explanations
from py_arg_visualisation.functions.explanations_functions.get_at_explanations import get_str_explanations
from py_arg_visualisation.functions.extensions_functions.get_accepted_formulas import get_accepted_formulas
from py_arg_visualisation.functions.extensions_functions.get_af_extensions import get_argumentation_framework_extensions
from py_arg_visualisation.functions.extensions_functions import get_argumentation_theory_extensions
from py_arg_visualisation.functions.graph_data_functions.get_at_graph_data import get_argumentation_theory_graph_data
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data
from py_arg_visualisation.functions.import_functions.read_argumentation_framework_functions import read_argumentation_framework
from py_arg_visualisation.functions.import_functions.read_argumentation_theory_functions import read_argumentation_theory
from py_arg_visualisation.layout_elements import get_layout_elements

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

app_layout, app_validation_layout, layout_abstract, layout_ASPIC = get_layout_elements(app)
app.layout = app_layout
app.validation_layout = app_validation_layout


@app.callback(
    dash.dependencies.Output('arg-layout', 'children'),
    [dash.dependencies.Input('arg-choice', 'value')]
)
def setting_choice(choice):
    if choice == 'Abstr':
        return layout_abstract
    elif choice == 'ASPIC':
        return layout_ASPIC


@app.callback(
    dash.dependencies.Output('abstr-arg-setting-collapse', 'is_open'),
    [dash.dependencies.Input('abstr-arg-setting-button', 'n_clicks')],
    [dash.dependencies.State('abstr-arg-setting-collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstr-evaluation-collapse', 'is_open'),
    [dash.dependencies.Input('abstr-evaluation-button', 'n_clicks')],
    [dash.dependencies.State('abstr-evaluation-collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstr-explanation-collapse', 'is_open'),
    [dash.dependencies.Input('abstr-explanation-button', 'n_clicks')],
    [dash.dependencies.State('abstr-explanation-collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstr-explanation-function', 'options'),
    [dash.dependencies.Input('abstr-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice):
    return [{'label': i, 'value': i} for i in EXPLANATION_FUNCTION_OPTIONS[choice]]


@app.callback(
    dash.dependencies.Output('str-arg-setting-collapse', 'is_open'),
    [dash.dependencies.Input('str-arg-setting-button', 'n_clicks')],
    [dash.dependencies.State('str-arg-setting-collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('str-evaluation-collapse', 'is_open'),
    [dash.dependencies.Input('str-evaluation-button', 'n_clicks')],
    [dash.dependencies.State('str-evaluation-collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('str-explanation-collapse', 'is_open'),
    [dash.dependencies.Input('str-explanation-button', 'n_clicks')],
    [dash.dependencies.State('str-explanation-collapse', 'is_open')],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('str-explanation-function', 'options'),
    [dash.dependencies.Input('str-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice):
    return [{'label': i, 'value': i} for i in EXPLANATION_FUNCTION_OPTIONS[choice]]


@app.callback(
    dash.dependencies.Output('abstr-output', 'children'),
    dash.dependencies.Output('abstrnet', 'data'),
    dash.dependencies.Input('abstrAF-Calc', 'n_clicks'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    prevent_initial_call=True
)
def create_AF(click, arguments, attacks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'abstrAF-Calc' in changed_id:
        arg_framework = read_argumentation_framework(arguments, attacks)
        data = get_argumentation_framework_graph_data(arg_framework)
        return html.Div([html.H4('The arguments of the AF:', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(arg_framework.arguments))]), data
    else:
        data = {'nodes': [], 'edges': []}
        return 'No argumentation setting was provided', data


@app.callback(
    dash.dependencies.Output('abstr-evaluation', 'children'),
    dash.dependencies.Input('abstrAF-Eval', 'n_clicks'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    dash.dependencies.State('abstr-evaluation-semantics', 'value'),
    dash.dependencies.State('abstr-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_abstrAF(click, arguments, attacks, semantics, strategy):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Eval' in changed_id:
        arg_framework = read_argumentation_framework(arguments, attacks)
        frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
        accepted = set()
        if semantics != 'Grd':
            extension = [set(frozen_extension) for frozen_extension in frozen_extensions]
            if strategy == 'Skep':
                accepted = set.intersection(*extension)
            elif strategy == 'Cred':
                accepted = set.union(*extension)
        elif semantics == 'Grd':
            extension = frozen_extensions
            accepted = extension
        return html.Div([html.H4('The extension(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(str(extension).replace('set()', '{}'))),
                         html.H4('The accepted argument(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(str(accepted).replace('set()', '{}')))])


@app.callback(
    dash.dependencies.Output('abstr-explanation', 'children'),
    dash.dependencies.Input('abstrAF-Expl', 'n_clicks'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    dash.dependencies.State('abstr-evaluation-semantics', 'value'),
    dash.dependencies.State('abstr-explanation-function', 'value'),
    dash.dependencies.State('abstr-explanation-type', 'value'),
    dash.dependencies.State('abstr-explanation-strategy', 'value'),
    prevent_initial_call=True
)
def derive_abstrExpl(click, arguments, attacks, semantics, function, expltype, strategy):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Expl' in changed_id:
        if semantics == '':
            return html.Div([html.H4('Error', style={'color': 'red'}),
                             'Choose a semantics under "Evaluation" before deriving explanations.'])
        else:
            arg_framework = read_argumentation_framework(arguments, attacks)
            output_str = ''
            frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
            accepted = set()
            if semantics != 'Grd':
                extension = [set(frozen_extension) for frozen_extension in frozen_extensions]
                if strategy == 'Skep':
                    accepted = set.intersection(*extension)
                elif strategy == 'Cred':
                    accepted = set.union(*extension)
            else:
                extension = frozen_extensions
                accepted = extension
            explanations = get_argumentation_framework_explanations(arg_framework, semantics, extension, accepted, function, expltype,
                                                                    strategy)
            return html.Div([html.H4('The Explanation(s):', style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(explanations).replace('set()', '{}')))])


@app.callback(
    dash.dependencies.Output('abstrnet-output', 'children'),
    dash.dependencies.Output('abstrnet-evaluation', 'children'),
    dash.dependencies.Output('abstrnet-explanation', 'children'),
    dash.dependencies.Input('abstrnet', 'selection'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    dash.dependencies.State('abstr-evaluation-semantics', 'value'),
    dash.dependencies.State('abstr-evaluation-strategy', 'value'),
    dash.dependencies.State('abstr-explanation-function', 'value'),
    dash.dependencies.State('abstr-explanation-type', 'value'),
    prevent_initial_call=True
)
def interactive_abstr_graph(selection, arguments, attacks, semantics, strategy, function, expltype):
    while selection is not None:
        arg_framework = read_argumentation_framework(arguments, attacks)
        for arg in arg_framework.arguments:
            if str(arg) == str(selection['nodes'][0]):
                argument = arg
        arg_ext = []
        output_arg = html.Div(
            [html.H4('The selected argument:', style={'color': '#152A47'}), html.H6('{}'.format(str(argument)))])
        output_accept = ''
        expl_output = ''
        output_evaluation = ''
        if semantics != '':
            frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
            if strategy != '':
                skep_accept = False
                cred_accept = False
                if semantics != 'Grd':
                    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
                    skep_accepted = set.intersection(*extensions)
                    cred_accepted = set.union(*extensions)
                    for ext in extensions:
                        if argument in ext:
                            arg_ext.append(ext)
                    if arg_ext == extensions:
                        skep_accept = True
                    if arg_ext != []:
                        cred_accept = True
                elif semantics == 'Grd':
                    extensions = frozen_extensions
                    if argument in extensions:
                        arg_ext.append(extensions)
                        skep_accepted = extensions
                        cred_accepted = extensions
                        skep_accept = True
                        cred_accept = True
                if skep_accept:
                    output_accept += str(argument) + ' is skeptically and credulously accepted.'
                    if function is not None and expltype == 'Acc':
                        skep_expla = get_argumentation_framework_explanations(arg_framework, semantics, extensions, skep_accepted,
                                                                              function, expltype, 'Skep')
                        cred_expla = get_argumentation_framework_explanations(arg_framework, semantics, extensions, cred_accepted,
                                                                              function, expltype, 'Cred')
                        expl_output = html.Div([html.H4(
                            'The skeptical acceptance explanation for {}:'.format(str(argument)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()', '{}'))), html.H4(
                                'The credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no non-acceptance explanation for argument {}, since it is '
                                                'skeptically accepted.'.format(
                                                    argument)])
                elif cred_accept:
                    output_accept += str(argument) + ' is credulously but not skeptically accepted.'
                    if function is not None and expltype == 'Acc':
                        cred_expla = get_argumentation_framework_explanations(arg_framework, semantics, extensions, cred_accepted,
                                                                              function, expltype, 'Cred')
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(argument)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        skep_expla = get_argumentation_framework_explanations(arg_framework, semantics, extensions, skep_accepted,
                                                                              function, expltype, 'Skep')
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(argument)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()', '{}')))])
                elif skep_accept == False and cred_accept == False:
                    output_accept += str(argument) + ' is neither  credulously nor skeptically accepted.'
                    if function is not None and expltype == 'NonAcc':
                        skep_expla = get_argumentation_framework_explanations(arg_framework, semantics, extensions, skep_accepted,
                                                                              function, expltype, 'Skep')
                        cred_expla = get_argumentation_framework_explanations(arg_framework, semantics, extensions, cred_accepted,
                                                                              function, expltype, 'Cred')
                        expl_output = html.Div([html.H4(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()', '{}'))), html.H4(
                                'The not credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and expltype == 'Acc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no acceptance explanation for argument {}, since it is not '
                                                'credulously accepted.'.format(
                                                    argument)])
            output_evaluation = html.Div(
                [html.H4('The extensions with argument {}:'.format(str(argument)), style={'color': '#152A47'}),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_arg, output_evaluation, expl_output
    raise PreventUpdate


@app.callback(
    dash.dependencies.Output('ordering-link', 'children'),
    dash.dependencies.Output('ordering-link', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
)
def choose_ordering(choice):
    if choice == 'nochoice':
        options = [{'label': 'None', 'value': 'nolink'},
                   {'label': 'Last link', 'value': 'lastl', 'disabled': True},
                   {'label': 'Weakest link', 'value': 'weakl', 'disabled': True}
                   ]
        return options, 'nolink'
    else:
        options = [{'label': 'None', 'value': 'nolink', 'state': 'disabled'},
                   {'label': 'Last link', 'value': 'lastl'},
                   {'label': 'Weakest link', 'value': 'weakl'}
                   ]
        return options, 'lastl'


@app.callback(
    dash.dependencies.Output('str-output', 'children'),
    dash.dependencies.Output('strnet', 'data'),
    dash.dependencies.Input('strAF-Calc', 'n_clicks'),
    dash.dependencies.State('aspic-axioms', 'value'),
    dash.dependencies.State('aspic-ordinary-premises', 'value'),
    dash.dependencies.State('aspic-strict-rules', 'value'),
    dash.dependencies.State('aspic-defeasible-rules', 'value'),
    dash.dependencies.State('ordinary-prem-preferences', 'value'),
    dash.dependencies.State('defeasible-rule-preferences', 'value'),
    dash.dependencies.State('ordering-choice', 'value'),
    dash.dependencies.State('ordering-link', 'value'),
    prevent_initial_call=True
)
def create_AT(click, axioms_str: str, ordinary_premises_str: str, strict_rules_str: str, defeasible_rules_str: str,
              ordinary_premise_preferences_str: str, defeasible_rule_preferences_str: str,
              ordering_choice_value: str, ordering_link_value: str):
    # Read the ordering
    ordering_specification = ordering_choice_value + ordering_link_value

    # Read the argumentation theory
    arg_theory, error_message = read_argumentation_theory(
        axioms_str, ordinary_premises_str, strict_rules_str, defeasible_rules_str, ordinary_premise_preferences_str,
        defeasible_rule_preferences_str)

    # Generate the graph data for this argumentation theory
    data = get_argumentation_theory_graph_data(arg_theory, ordering_specification)

    # Generate the list of arguments
    generated_arguments_html_content = \
        [html.H4('The generated argument(s):', style={'color': '#152A47'}),
         html.Ul([html.Li(argument.short_name) for argument in arg_theory.all_arguments])
         ]
    return generated_arguments_html_content, data


@app.callback(
    dash.dependencies.Output('str-evaluation', 'children'),
    dash.dependencies.Input('strAF-Eval', 'n_clicks'),
    dash.dependencies.State('aspic-axioms', 'value'),
    dash.dependencies.State('aspic-ordinary-premises', 'value'),
    dash.dependencies.State('aspic-strict-rules', 'value'),
    dash.dependencies.State('aspic-defeasible-rules', 'value'),
    dash.dependencies.State('ordinary-prem-preferences', 'value'),
    dash.dependencies.State('defeasible-rule-preferences', 'value'),
    dash.dependencies.State('ordering-choice', 'value'),
    dash.dependencies.State('ordering-link', 'value'),
    dash.dependencies.State('str-evaluation-semantics', 'value'),
    dash.dependencies.State('str-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_strAF(click, axioms_str: str, ordinary_premises_str: str, strict_rules_str: str, defeasible_rules_str: str,
                   ordinary_premise_preferences_str: str, defeasible_rule_preferences_str: str,
                   ordering_choice_value: str, ordering_link_value: str,
                   semantics_specification: str, acceptance_strategy_specification: str):
    # Read the ordering
    ordering_specification = ordering_choice_value + ordering_link_value

    # Read the argumentation theory
    arg_theory, error_message = read_argumentation_theory(
        axioms_str, ordinary_premises_str, strict_rules_str, defeasible_rules_str, ordinary_premise_preferences_str,
        defeasible_rule_preferences_str)

    frozen_extensions = get_argumentation_theory_extensions(arg_theory, semantics_specification, ordering_specification)

    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
    accepted_formulas = get_accepted_formulas(extensions, acceptance_strategy_specification)

    return [html.H4('The extension(s):', style={'color': '#152A47'}),
            html.Ul([html.Li('{' + ', '.join(argument.short_name for argument in extension) + '}')
                     for extension in extensions]),
            html.H4('The accepted formula(s):', style={'color': '#152A47'}),
            html.Ul([html.Li(accepted_formula.s1) for accepted_formula in sorted(accepted_formulas)])]


@app.callback(
    dash.dependencies.Output('str-explanation', 'children'),
    dash.dependencies.Input('strAF-Expl', 'n_clicks'),
    dash.dependencies.State('aspic-axioms', 'value'),
    dash.dependencies.State('aspic-ordinary-premises', 'value'),
    dash.dependencies.State('aspic-strict-rules', 'value'),
    dash.dependencies.State('aspic-defeasible-rules', 'value'),
    dash.dependencies.State('ordinary-prem-preferences', 'value'),
    dash.dependencies.State('defeasible-rule-preferences', 'value'),
    dash.dependencies.State('ordering-choice', 'value'),
    dash.dependencies.State('ordering-link', 'value'),
    dash.dependencies.State('str-evaluation-semantics', 'value'),
    dash.dependencies.State('str-explanation-function', 'value'),
    dash.dependencies.State('str-explanation-type', 'value'),
    dash.dependencies.State('str-explanation-strategy', 'value'),
    dash.dependencies.State('str-explanation-form', 'value'),
    prevent_initial_call=True
)
def derive_strExpl(click, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences, choice, link,
                   semantics, function, expltype, strategy, form):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Expl' in changed_id:
        if semantics == '':
            return html.Div([html.H4('Error', style={'color': 'red'}),
                             'Choose a semantics under "Evaluation" before deriving explanations.'])
        else:
            ordering = choice + link
            arg_theory, error_message = read_argumentation_theory(axioms, ordinary, strict, defeasible,
                                                                  premise_preferences, rule_preferences)
            if error_message != '':
                return error_message
            frozen_extensions = get_argumentation_theory_extensions(arg_theory, semantics, ordering)
            accepted = set()
            if semantics != 'Grd':
                extension = [set(frozen_extension) for frozen_extension in frozen_extensions]
                accepted = get_accepted_formulas(extension, strategy)
            elif semantics == 'Grd':
                extension = frozen_extensions
                accepted = extension
            explanations = get_str_explanations(arg_theory, semantics, ordering, extension, accepted, function,
                                                expltype,
                                                strategy, form)

            return html.Div([html.H4('The Explanation(s):', style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(explanations).replace('set()','{}')))])


@app.callback(
    dash.dependencies.Output('strnet-output', 'children'),
    dash.dependencies.Output('strnet-evaluation', 'children'),
    dash.dependencies.Output('strnet-explanation', 'children'),
    dash.dependencies.Input('strnet', 'selection'),
    dash.dependencies.Input('strnet', 'data'),
    dash.dependencies.Input('aspic-axioms', 'value'),
    dash.dependencies.Input('aspic-ordinary-premises', 'value'),
    dash.dependencies.Input('aspic-strict-rules', 'value'),
    dash.dependencies.Input('aspic-defeasible-rules', 'value'),
    dash.dependencies.Input('ordinary-prem-preferences', 'value'),
    dash.dependencies.Input('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
    dash.dependencies.Input('ordering-link', 'value'),
    dash.dependencies.Input('str-evaluation-semantics', 'value'),
    dash.dependencies.Input('str-explanation-function', 'value'),
    dash.dependencies.Input('str-explanation-type', 'value'),
    dash.dependencies.Input('str-evaluation-strategy', 'value'),
    dash.dependencies.Input('str-explanation-form', 'value'),
    prevent_initial_call=True
)
def interactive_str_graph(selection, data, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences,
                          choice, link,
                          semantics, function, expltype, strategy, form):
    while selection is not None:
        ordering = choice + link
        arg_theory, error_message = read_argumentation_theory(axioms, ordinary, strict, defeasible, premise_preferences,
                                                              rule_preferences)
        if error_message != '':
            return error_message
        select_id = selection['nodes'][0]
        for node in data['nodes']:
            if node.get('id') == select_id:
                select_node = node.get('label')
        for arg in arg_theory.all_arguments:
            if str(arg) == str(select_node):
                argument = arg
                formula = arg.conclusion
        arg_ext = []
        output_arg = html.Div(
            [html.H4('The selected argument:', style={'color': '#152A47'}), html.H6('{}'.format(str(argument))),
             html.H4('The selected conclusion:', style={'color': '#152A47'}),
             html.H6('{}'.format(str(argument.conclusion)))])
        output_accept = ''
        expl_output = ''
        output_evaluation = ''
        if semantics != '':
            frozen_extensions = get_argumentation_theory_extensions(arg_theory, semantics, ordering)
            if strategy != '':
                skep_accept = False
                wskep_accept = False
                cred_accept = False
                if semantics != 'Grd':
                    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
                    skep_accepted = get_accepted_formulas(extensions, 'Skep')
                    wskep_accepted = get_accepted_formulas(extensions, 'WSkep')
                    cred_accepted = get_accepted_formulas(extensions, 'Cred')
                    for ext in extensions:
                        if argument in ext:
                            arg_ext.append(ext)
                    if formula in skep_accepted:
                        skep_accept = True
                    if formula in wskep_accepted:
                        wskep_accept = True
                    if formula in cred_accepted:
                        cred_accept = True
                elif semantics == 'Grd':
                    extensions = frozen_extensions
                    if argument in extensions:
                        arg_ext.append(extensions)
                        skep_accepted = extensions
                        cred_accepted = extensions
                        skep_accept = True
                        wskep_accept = True
                        cred_accept = True
                if skep_accept:
                    output_accept += str(formula) + ' is (weakly) skeptically and credulously accepted.'
                    if function is not None and expltype == 'Acc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div([html.H4(
                            'The skeptical acceptance explanation for {}:'.format(str(formula)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}'))), html.H4(
                                'The credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no non-acceptance explanation for formula {}, since it is '
                                                'skeptically accepted.'.format(
                                                    formula)])
                elif wskep_accept:
                    output_accept += str(
                        formula) + ' is weakly skeptically and credulously accepted, but not skeptically accepted.'
                    if function is not None and expltype == 'Acc':
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}')))])
                elif cred_accept:
                    output_accept += str(formula) + ' is credulously but not (weakly) skeptically accepted.'
                    if function is not None and expltype == 'Acc':
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}')))])
                elif skep_accept == False and cred_accept == False:
                    output_accept += str(argument) + ' is neither credulously nor (weakly) skeptically accepted.'
                    if function is not None and expltype == 'NonAcc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div([html.H4(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()','{}'))), html.H4(
                                'The not credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()','{}')))])
                    elif function is not None and expltype == 'Acc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no acceptance explanation for formula {}, since it is not '
                                                'credulously accepted.'.format(
                                                    formula)])
            output_evaluation = html.Div(
                [html.H4('The extensions with argument {}:'.format(str(argument)), style={'color': '#152A47'}),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_arg, output_evaluation, expl_output
    raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
