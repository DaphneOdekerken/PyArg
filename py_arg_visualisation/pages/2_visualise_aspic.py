import json
from typing import List

import dash
from dash import html, callback, Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.argumentation_theory_generators.argumentation_theory_generator import \
    ArgumentationTheoryGenerator
from py_arg_visualisation.functions.explanations_functions.explanation_function_options import \
    EXPLANATION_FUNCTION_OPTIONS
from py_arg_visualisation.functions.explanations_functions.get_at_explanations import get_str_explanations
from py_arg_visualisation.functions.extensions_functions.get_accepted_formulas import get_accepted_formulas
from py_arg_visualisation.functions.extensions_functions.get_at_extensions import get_argumentation_theory_extensions
from py_arg_visualisation.functions.graph_data_functions.get_at_graph_data import get_argumentation_theory_graph_data
from py_arg_visualisation.functions.import_functions.read_argumentation_theory_functions import \
    read_argumentation_theory
from py_arg_visualisation.layout_elements.structured_argumentation_layout_elements import get_aspic_setting, \
    get_structured_evaluation, get_structured_explanation, get_aspic_layout

dash.register_page(__name__, name='Visualise ASPIC+ AT', title='Visualise ASPIC+ AT')


ASPIC_setting = get_aspic_setting()
ASPIC_evaluation = get_structured_evaluation()
ASPIC_explanation = get_structured_explanation()
layout_ASPIC = get_aspic_layout(ASPIC_setting, ASPIC_evaluation, ASPIC_explanation)

layout = html.Div(
    children=[
        html.H1('Visualisation of ASPIC+ argumentation theories'),
        layout_ASPIC
    ]
)


@callback(
    Output('structured-arg-setting-collapse', 'is_open'),
    [Input('structured-arg-setting-button', 'n_clicks')],
    [State('structured-arg-setting-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@callback(
    Output('structured-evaluation-collapse', 'is_open'),
    [Input('structured-evaluation-button', 'n_clicks')],
    [State('structured-evaluation-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@callback(
    Output('structured-explanation-collapse', 'is_open'),
    [Input('structured-explanation-button', 'n_clicks')],
    [State('structured-explanation-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@callback(
    Output('structured-explanation-function', 'options'),
    [Input('structured-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice: str):
    return [{'label': i, 'value': i} for i in EXPLANATION_FUNCTION_OPTIONS[choice]]


@callback(
    Output('aspic-axioms', 'value'),
    Output('aspic-ordinary-premises', 'value'),
    Output('aspic-strict-rules', 'value'),
    Output('aspic-defeasible-rules', 'value'),
    Output('ordinary-prem-preferences', 'value'),
    Output('defeasible-rule-preferences', 'value'),
    Input('generate-random-arg-theory-button', 'n_clicks')
)
def generate_random_argumentation_theory(nr_of_clicks: int):
    if nr_of_clicks > 0:
        argumentation_system_generator = LayeredArgumentationSystemGenerator(
            nr_of_literals=10, nr_of_rules=5,
            rule_antecedent_distribution={1: 4, 2: 1},
            literal_layer_distribution={0: 5, 1: 3, 2: 2},
            strict_rule_ratio=0.3
        )
        argumentation_system = argumentation_system_generator.generate()
        argumentation_theory_generator = ArgumentationTheoryGenerator(argumentation_system,
                                                                      knowledge_literal_ratio=0.4,
                                                                      axiom_knowledge_ratio=0.5)
        argumentation_theory = argumentation_theory_generator.generate()
        aspic_axioms_value = '\n'.join(str(axiom) for axiom in argumentation_theory.knowledge_base_axioms)
        aspic_ordinary_premises_value = '\n'.join(str(premise)
                                                  for premise in argumentation_theory.knowledge_base_ordinary_premises)
        aspic_strict_rule = '\n'.join(str(strict_rule)
                                      for strict_rule in argumentation_system.strict_rules)
        aspic_defeasible_rule = '\n'.join(f'{defeasible_rule.id}: {str(defeasible_rule)}'
                                          for defeasible_rule in argumentation_system.defeasible_rules)
        aspic_ordinary_premise_preference_value = \
            '\n'.join(f'{str(preference[0])} < {str(preference[1])}'
                      for preference in argumentation_theory.ordinary_premise_preferences.preference_tuples)
        aspic_defeasible_rule_preference_vale = \
            '\n'.join(f'{preference[0].id} < {preference[1].id}'
                      for preference in argumentation_system.rule_preferences.preference_tuples)
        return aspic_axioms_value, aspic_ordinary_premises_value, aspic_strict_rule, aspic_defeasible_rule, \
               aspic_ordinary_premise_preference_value, aspic_defeasible_rule_preference_vale
    return '', '', '', '', '', ''


@callback(
    Output('structured-output', 'children'),
    Output('structured-argumentation-graph', 'data'),
    Input('create-argumentation-theory-button', 'n_clicks'),
    State('aspic-axioms', 'value'),
    State('aspic-ordinary-premises', 'value'),
    State('aspic-strict-rules', 'value'),
    State('aspic-defeasible-rules', 'value'),
    State('ordinary-prem-preferences', 'value'),
    State('defeasible-rule-preferences', 'value'),
    State('ordering-choice', 'value'),
    State('ordering-link', 'value'),
    Input('selected-argument-store-structured', 'data'),
    prevent_initial_call=True
)
def create_argumentation_theory(_nr_of_clicks: int, axioms_str: str, ordinary_premises_str: str, strict_rules_str: str,
                                defeasible_rules_str: str,
                                ordinary_premise_preferences_str: str, defeasible_rule_preferences_str: str,
                                ordering_choice_value: str, ordering_link_value: str,
                                selected_arguments: List[str]):
    # Read the ordering
    ordering_specification = ordering_choice_value + ordering_link_value

    # Read the argumentation theory
    arg_theory, error_message = read_argumentation_theory(
        axioms_str, ordinary_premises_str, strict_rules_str, defeasible_rules_str, ordinary_premise_preferences_str,
        defeasible_rule_preferences_str)

    # Generate the graph data for this argumentation theory
    data = get_argumentation_theory_graph_data(arg_theory, ordering_specification, selected_arguments)

    # Generate the list of arguments
    generated_arguments_html_content = \
        [html.H4('The generated argument(s):'),
         html.Ul([html.Li(argument.short_name) for argument in arg_theory.all_arguments])
         ]
    return generated_arguments_html_content, data


@callback(
    Output('structured-evaluation', 'children'),
    Input('evaluate-structured-argumentation-theory-button', 'n_clicks'),
    State('aspic-axioms', 'value'),
    State('aspic-ordinary-premises', 'value'),
    State('aspic-strict-rules', 'value'),
    State('aspic-defeasible-rules', 'value'),
    State('ordinary-prem-preferences', 'value'),
    State('defeasible-rule-preferences', 'value'),
    State('ordering-choice', 'value'),
    State('ordering-link', 'value'),
    State('structured-evaluation-semantics', 'value'),
    State('structured-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_structured_argumentation_framework(_nr_of_clicks: int, axioms_str: str, ordinary_premises_str: str,
                                                strict_rules_str: str, defeasible_rules_str: str,
                                                ordinary_premise_preferences_str: str,
                                                defeasible_rule_preferences_str: str,
                                                ordering_choice_value: str, ordering_link_value: str,
                                                semantics_specification: str, acceptance_strategy_specification: str):
    # Read the ordering
    ordering_specification = ordering_choice_value + ordering_link_value

    # Read the argumentation theory
    arg_theory, error_message = read_argumentation_theory(
        axioms_str, ordinary_premises_str, strict_rules_str, defeasible_rules_str, ordinary_premise_preferences_str,
        defeasible_rule_preferences_str)
    if not arg_theory.all_arguments:
        raise PreventUpdate

    frozen_extensions = get_argumentation_theory_extensions(arg_theory, semantics_specification, ordering_specification)

    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
    accepted_formulas = get_accepted_formulas(extensions, acceptance_strategy_specification)

    extension_list_items = []
    for extension in extensions:
        extension_readable_str = '{' + ', '.join(argument.short_name for argument in extension) + '}'
        extension_long_str = '+'.join(argument.name for argument in extension)
        extension_with_link = html.A(children=extension_readable_str,
                                     id={'type': 'extension-button', 'index': extension_long_str})
        extension_list_items.append(html.Li(extension_with_link))

    return [html.H4('The extension(s):'),
            html.Ul(extension_list_items),
            html.H4('The accepted formula(s):'),
            html.Ul([html.Li(accepted_formula.s1) for accepted_formula in sorted(accepted_formulas)])]


@callback(
    Output('selected-argument-store-structured', 'data'),
    Input({'type': 'extension-button', 'index': ALL}, 'n_clicks'),
    State('selected-argument-store-structured', 'data'),
)
def mark_extension_in_graph(nr_of_clicks_values,
                            old_selected_data: List[str]):
    button_clicked_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_clicked_id == '':
        return old_selected_data
    if nr_of_clicks_values[0] is None:
        raise PreventUpdate
    button_clicked_id_content = json.loads(button_clicked_id)
    button_clicked_id_index = button_clicked_id_content['index']
    extension_arguments = button_clicked_id_index.split('+')
    return extension_arguments


@callback(
    Output('selected-argument-store-abstract', 'data'),
    Input({'type': 'extension-button-abstract', 'index': ALL}, 'n_clicks'),
    State('selected-argument-store-abstract', 'data'),
)
def mark_extension_in_graph(nr_of_clicks_values,
                            old_selected_data: List[str]):
    button_clicked_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_clicked_id == '':
        return old_selected_data
    if nr_of_clicks_values[0] is None:
        raise PreventUpdate
    button_clicked_id_content = json.loads(button_clicked_id)
    button_clicked_id_index = button_clicked_id_content['index']
    extension_arguments = button_clicked_id_index.split('+')
    return extension_arguments


@callback(
    Output('structured-explanation', 'children'),
    Input('structured-explanation-button', 'n_clicks'),
    State('aspic-axioms', 'value'),
    State('aspic-ordinary-premises', 'value'),
    State('aspic-strict-rules', 'value'),
    State('aspic-defeasible-rules', 'value'),
    State('ordinary-prem-preferences', 'value'),
    State('defeasible-rule-preferences', 'value'),
    State('ordering-choice', 'value'),
    State('ordering-link', 'value'),
    State('structured-evaluation-semantics', 'value'),
    State('structured-explanation-function', 'value'),
    State('structured-explanation-type', 'value'),
    State('structured-explanation-strategy', 'value'),
    State('structured-explanation-form', 'value'),
    prevent_initial_call=True
)
def derive_explanation_structured(_nr_of_clicks: int, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences,
                                  choice, link, semantics, function, explanation_type, strategy, form):
    if semantics == '':
        return html.Div([html.H4('Error', className='error'),
                         'Choose a semantics under "Evaluation" before deriving explanations.'])
    else:
        ordering = choice + '_' + link
        arg_theory, error_message = read_argumentation_theory(axioms, ordinary, strict, defeasible,
                                                              premise_preferences, rule_preferences)
        if error_message != '':
            return error_message
        frozen_extensions = get_argumentation_theory_extensions(arg_theory, semantics, ordering)
        accepted = set()
        if semantics != 'Grounded':
            extension = [set(frozen_extension) for frozen_extension in frozen_extensions]
            accepted = get_accepted_formulas(extension, strategy)
        elif semantics == 'Grounded':
            extension = frozen_extensions
            accepted = extension
        explanations = get_str_explanations(arg_theory, semantics, ordering, extension, accepted, function,
                                            explanation_type,
                                            strategy, form)

        return html.Div([html.H4('The Explanation(s):'),
                         html.H6('\n {}'.format(str(explanations).replace('set()','{}')))])


@callback(
    Output('structured-argumentation-graph-output', 'children'),
    Output('structured-argumentation-graph-evaluation', 'children'),
    Output('structured-argumentation-graph-explanation', 'children'),
    Input('structured-argumentation-graph', 'selection'),
    Input('structured-argumentation-graph', 'data'),
    Input('aspic-axioms', 'value'),
    Input('aspic-ordinary-premises', 'value'),
    Input('aspic-strict-rules', 'value'),
    Input('aspic-defeasible-rules', 'value'),
    Input('ordinary-prem-preferences', 'value'),
    Input('defeasible-rule-preferences', 'value'),
    Input('ordering-choice', 'value'),
    Input('ordering-link', 'value'),
    Input('structured-evaluation-semantics', 'value'),
    Input('structured-explanation-function', 'value'),
    Input('structured-explanation-type', 'value'),
    Input('structured-evaluation-strategy', 'value'),
    Input('structured-explanation-form', 'value'),
    prevent_initial_call=True
)
def interactive_str_graph(selection, data, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences,
                          choice, link,
                          semantics, function, explanation_type, strategy, form):
    while selection is not None:
        ordering = choice + '_' + link
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
            [html.H4('The selected argument:'), html.H6('{}'.format(str(argument))),
             html.H4('The selected conclusion:'),
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
                if semantics != 'Grounded':
                    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
                    skep_accepted = get_accepted_formulas(extensions, 'Skeptical')
                    wskep_accepted = get_accepted_formulas(extensions, 'WeaklySkeptical')
                    cred_accepted = get_accepted_formulas(extensions, 'Credulous')
                    for ext in extensions:
                        if argument in ext:
                            arg_ext.append(ext)
                    if formula in skep_accepted:
                        skep_accept = True
                    if formula in wskep_accepted:
                        wskep_accept = True
                    if formula in cred_accepted:
                        cred_accept = True
                elif semantics == 'Grounded':
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
                    if function is not None and explanation_type == 'Acceptance':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, explanation_type, 'Skeptical', form)
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, explanation_type, 'Credulous', form)
                        expl_output = html.Div([html.H4(
                            'The skeptical acceptance explanation for {}:'.format(str(formula))),
                            html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}'))), html.H4(
                                'The credulous acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        expl_output = html.Div([html.H4('Error', className='error'),
                                                'There is no non-acceptance explanation for formula {}, since it is '
                                                'skeptically accepted.'.format(
                                                    formula)])
                elif wskep_accept:
                    output_accept += str(
                        formula) + ' is weakly skeptically and credulously accepted, but not skeptically accepted.'
                    if function is not None and explanation_type == 'Acceptance':
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, explanation_type, 'Credulous', form)
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(formula))),
                             html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, explanation_type, 'Skeptical', form)
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(formula))),
                             html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}')))])
                elif cred_accept:
                    output_accept += str(formula) + ' is credulously but not (weakly) skeptically accepted.'
                    if function is not None and explanation_type == 'Acceptance':
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, explanation_type, 'Credulous', form)
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(formula))),
                             html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, explanation_type, 'Skeptical', form)
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(formula))),
                             html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}')))])
                elif skep_accept == False and cred_accept == False:
                    output_accept += str(argument) + ' is neither credulously nor (weakly) skeptically accepted.'
                    if function is not None and explanation_type == 'NonAcceptance':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, explanation_type, 'Skeptical', form)
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, explanation_type, 'Credulous', form)
                        expl_output = html.Div([html.H4(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()','{}'))), html.H4(
                                'The not credulous acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()','{}')))])
                    elif function is not None and explanation_type == 'Acceptance':
                        expl_output = html.Div([html.H4('Error', className='error'),
                                                'There is no acceptance explanation for formula {}, since it is not '
                                                'credulously accepted.'.format(
                                                    formula)])
            output_evaluation = html.Div(
                [html.H4('The extensions with argument {}:'.format(str(argument))),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_arg, output_evaluation, expl_output
    raise PreventUpdate
