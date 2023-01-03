import json
from typing import List

from dash import html
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate

import dash.dependencies

from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.generators.argumentation_theory_generators.argumentation_theory_generator import \
    ArgumentationTheoryGenerator
from py_arg_visualisation.functions.explanations_functions.explanation_function_options import \
    EXPLANATION_FUNCTION_OPTIONS
from py_arg_visualisation.functions.explanations_functions.get_af_explanations import \
    get_argumentation_framework_explanations
from py_arg_visualisation.functions.explanations_functions.get_at_explanations import get_str_explanations
from py_arg_visualisation.functions.extensions_functions.get_accepted_formulas import get_accepted_formulas
from py_arg_visualisation.functions.extensions_functions.get_af_extensions import get_argumentation_framework_extensions
from py_arg_visualisation.functions.extensions_functions.get_at_extensions import get_argumentation_theory_extensions
from py_arg_visualisation.functions.graph_data_functions.get_at_graph_data import get_argumentation_theory_graph_data
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data
from py_arg_visualisation.functions.import_functions.read_argumentation_framework_functions import \
    read_argumentation_framework
from py_arg_visualisation.functions.import_functions.read_argumentation_theory_functions import \
    read_argumentation_theory
from py_arg_visualisation.layout_elements.layout_elements import get_layout_elements

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

app_layout, app_validation_layout, layout_abstract, layout_ASPIC = get_layout_elements(app)
app.layout = app_layout
app.validation_layout = app_validation_layout


@app.callback(
    dash.dependencies.Output('arg-layout', 'children'),
    [dash.dependencies.Input('arg-choice', 'value')]
)
def setting_choice(choice: str):
    if choice == 'Abstract':
        return layout_abstract
    elif choice == 'ASPIC':
        return layout_ASPIC


@app.callback(
    dash.dependencies.Output('abstract-arg-setting-collapse', 'is_open'),
    [dash.dependencies.Input('abstract-arg-setting-button', 'n_clicks')],
    [dash.dependencies.State('abstract-arg-setting-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstract-evaluation-collapse', 'is_open'),
    [dash.dependencies.Input('abstract-evaluation-button', 'n_clicks')],
    [dash.dependencies.State('abstract-evaluation-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstract-explanation-collapse', 'is_open'),
    [dash.dependencies.Input('abstract-explanation-button', 'n_clicks')],
    [dash.dependencies.State('abstract-explanation-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstract-explanation-function', 'options'),
    [dash.dependencies.Input('abstract-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice: str):
    return [{'label': i, 'value': i} for i in EXPLANATION_FUNCTION_OPTIONS[choice]]


@app.callback(
    dash.dependencies.Output('structured-arg-setting-collapse', 'is_open'),
    [dash.dependencies.Input('structured-arg-setting-button', 'n_clicks')],
    [dash.dependencies.State('structured-arg-setting-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('structured-evaluation-collapse', 'is_open'),
    [dash.dependencies.Input('structured-evaluation-button', 'n_clicks')],
    [dash.dependencies.State('structured-evaluation-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('structured-explanation-collapse', 'is_open'),
    [dash.dependencies.Input('structured-explanation-button', 'n_clicks')],
    [dash.dependencies.State('structured-explanation-collapse', 'is_open')],
)
def toggle_collapse(n: int, is_open: bool):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('structured-explanation-function', 'options'),
    [dash.dependencies.Input('structured-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice: str):
    return [{'label': i, 'value': i} for i in EXPLANATION_FUNCTION_OPTIONS[choice]]


@app.callback(
    dash.dependencies.Output('abstract-arguments', 'value'),
    dash.dependencies.Output('abstract-attacks', 'value'),
    dash.dependencies.Input('generate-random-af-button', 'n_clicks')
)
def generate_abstract_argumentation_framework(nr_of_clicks: int):
    if nr_of_clicks > 0:
        random_af = AbstractArgumentationFrameworkGenerator(8, 8, True).generate()
        abstract_arguments_value = '\n'.join((str(arg) for arg in random_af.arguments))
        abstract_attacks_value = '\n'.join((f'({str(defeat.from_argument)},{str(defeat.to_argument)})'
                                            for defeat in random_af.defeats))
        return abstract_arguments_value, abstract_attacks_value
    return '', ''


@app.callback(
    dash.dependencies.Output('abstract-arguments-output', 'children'),
    dash.dependencies.Output('abstract-argumentation-graph', 'data'),
    dash.dependencies.Input('create-argumentation-framework-button', 'n_clicks'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    prevent_initial_call=True
)
def create_abstract_argumentation_framework(_nr_of_clicks: int, arguments: str, attacks: str):
    arg_framework = read_argumentation_framework(arguments, attacks)
    data = get_argumentation_framework_graph_data(arg_framework)
    return html.Div([html.H4('The arguments of the AF:'),
                     html.Ul([html.Li(argument.name) for argument in arg_framework.arguments])]), data


@app.callback(
    dash.dependencies.Output('abstract-evaluation', 'children'),
    dash.dependencies.Input('evaluate-argumentation-framework-button', 'n_clicks'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    dash.dependencies.State('abstract-evaluation-semantics', 'value'),
    dash.dependencies.State('abstract-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_abstract_argumentation_framework(_nr_of_clicks: int, arguments: str, attacks: str, semantics: str,
                                              strategy: str):
    arg_framework = read_argumentation_framework(arguments, attacks)
    frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
    if strategy == 'Skeptical':
        accepted = set.intersection(*extensions)
    elif strategy == 'Credulous':
        accepted = set.union(*extensions)
    else:
        raise NotImplementedError

    return html.Div([html.H4('The extension(s):'),
                     html.Ul([html.Li('{' + ', '.join([argument.name for argument in extension]) + '}')
                              for extension in extensions]),
                     html.H4('The accepted argument(s):'),
                     html.Ul([html.Li(argument.name) for argument in accepted])
                     ])


@app.callback(
    dash.dependencies.Output('abstract-explanation', 'children'),
    dash.dependencies.Input('abstract-explanation-button', 'n_clicks'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    dash.dependencies.State('abstract-evaluation-semantics', 'value'),
    dash.dependencies.State('abstract-explanation-function', 'value'),
    dash.dependencies.State('abstract-explanation-type', 'value'),
    dash.dependencies.State('abstract-explanation-strategy', 'value'),
    prevent_initial_call=True
)
def derive_explanations_abstract_argumentation_framework(_nr_of_clicks: int, arguments: str, attacks: str,
                                                         semantics: str, explanation_function: str,
                                                         explanation_type: str, explanation_strategy: str):
    if semantics == '':
        return html.Div([html.H4('Error', className='error'),
                         'Choose a semantics under "Evaluation" before deriving explanations.'])
    else:
        arg_framework = read_argumentation_framework(arguments, attacks)
        frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
        extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
        if explanation_strategy == 'Skeptical':
            accepted_arguments = set.intersection(*extensions)
        elif explanation_strategy == 'Credulous':
            accepted_arguments = set.union(*extensions)
        else:
            raise NotImplementedError

        explanations = get_argumentation_framework_explanations(
            arg_framework, semantics, extensions, accepted_arguments,
            explanation_function, explanation_type, explanation_strategy)

        return html.Div([html.H4('The explanation(s):'),
                         html.Ul([html.Li(str(explanation)) for explanation in explanations])])


@app.callback(
    dash.dependencies.Output('abstract-argumentation-graph-output', 'children'),
    dash.dependencies.Output('abstract-argumentation-graph-evaluation', 'children'),
    dash.dependencies.Output('abstract-argumentation-graph-explanation', 'children'),
    dash.dependencies.Input('abstract-argumentation-graph', 'selection'),
    dash.dependencies.State('abstract-arguments', 'value'),
    dash.dependencies.State('abstract-attacks', 'value'),
    dash.dependencies.State('abstract-evaluation-semantics', 'value'),
    dash.dependencies.State('abstract-evaluation-strategy', 'value'),
    dash.dependencies.State('abstract-explanation-function', 'value'),
    dash.dependencies.State('abstract-explanation-type', 'value'),
    prevent_initial_call=True
)
def handle_selection_in_abstract_argumentation_graph(selection, arguments, attacks, semantics, strategy, function,
                                                     explanation_type):
    while selection is not None:
        arg_framework = read_argumentation_framework(arguments, attacks)
        for arg in arg_framework.arguments:
            if str(arg) == str(selection['nodes'][0]):
                argument = arg
        arg_ext = []
        output_arg = html.Div(
            [html.H4('The selected argument:'), html.H6('{}'.format(str(argument)))])
        output_accept = ''
        explanation_output = ''
        output_evaluation = ''
        if semantics != '':
            frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
            if strategy != '':
                skeptically_accepted = False
                credulously_accepted = False
                if semantics != 'Grounded':
                    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
                    skeptically_accepted_arguments = set.intersection(*extensions)
                    credulously_accepted_arguments = set.union(*extensions)
                    for ext in extensions:
                        if argument in ext:
                            arg_ext.append(ext)
                    if arg_ext == extensions:
                        skeptically_accepted = True
                    if arg_ext:
                        credulously_accepted = True
                elif semantics == 'Grounded':
                    extensions = frozen_extensions
                    if argument in extensions:
                        arg_ext.append(extensions)
                        skeptically_accepted_arguments = extensions
                        credulously_accepted_arguments = extensions
                        skeptically_accepted = True
                        credulously_accepted = True
                if skeptically_accepted:
                    output_accept += str(argument) + ' is skeptically and credulously accepted.'
                    if function is not None and explanation_type == 'Acceptance':
                        skeptical_explanation = get_argumentation_framework_explanations(
                            arg_framework, semantics, extensions, skeptically_accepted_arguments,
                            function, explanation_type, 'Skeptical')
                        credulous_explanation = get_argumentation_framework_explanations(
                            arg_framework, semantics, extensions, credulously_accepted_arguments,
                            function, explanation_type, 'Credulous')
                        explanation_output = html.Div([html.H4(
                            'The skeptical acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(
                                str(skeptical_explanation.get(str(argument))).replace('set()', '{}'))), html.H4(
                                'The credulous acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(
                                str(credulous_explanation.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        explanation_output = html.Div(
                            [html.H4('Error', className='error'),
                             'There is no non-acceptance explanation for argument {}, since it is '
                             'skeptically accepted.'.format(argument)])
                elif credulously_accepted:
                    output_accept += str(argument) + ' is credulously but not skeptically accepted.'
                    if function is not None and explanation_type == 'Acceptance':
                        credulous_explanation = get_argumentation_framework_explanations(
                            arg_framework, semantics, extensions, credulously_accepted_arguments,
                            function, explanation_type, 'Credulous')
                        explanation_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(argument))),
                             html.H6('\n {}'.format(
                                 str(credulous_explanation.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        skeptical_explanation = get_argumentation_framework_explanations(
                            arg_framework, semantics, extensions, skeptically_accepted_arguments,
                            function, explanation_type, 'Skeptical')
                        explanation_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(argument))),
                             html.H6('\n {}'.format(
                                 str(skeptical_explanation.get(str(argument))).replace('set()', '{}')))])
                elif not skeptically_accepted and not credulously_accepted:
                    output_accept += str(argument) + ' is neither  credulously nor skeptically accepted.'
                    if function is not None and explanation_type == 'NonAcceptance':
                        skeptical_explanation = get_argumentation_framework_explanations(
                            arg_framework, semantics, extensions, skeptically_accepted_arguments,
                            function, explanation_type, 'Skeptical')
                        credulous_explanation = get_argumentation_framework_explanations(
                            arg_framework, semantics, extensions, credulously_accepted_arguments,
                            function, explanation_type, 'Credulous')
                        explanation_output = html.Div([html.H4(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(skeptical_explanation.get(str(argument))).replace('set()', '{}'))), html.H4(
                                'The not credulous acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(credulous_explanation.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and explanation_type == 'Acceptance':
                        explanation_output = html.Div(
                            [html.H4('Error', className='error'),
                             'There is no acceptance explanation for argument {}, since it is not '
                             'credulously accepted.'.format(argument)])
            output_evaluation = html.Div(
                [html.H4('The extensions with argument {}:'.format(str(argument))),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_arg, output_evaluation, explanation_output
    raise PreventUpdate


@app.callback(
    dash.dependencies.Output('aspic-axioms', 'value'),
    dash.dependencies.Output('aspic-ordinary-premises', 'value'),
    dash.dependencies.Output('aspic-strict-rules', 'value'),
    dash.dependencies.Output('aspic-defeasible-rules', 'value'),
    dash.dependencies.Output('ordinary-prem-preferences', 'value'),
    dash.dependencies.Output('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('generate-random-arg-theory-button', 'n_clicks')
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


@app.callback(
    dash.dependencies.Output('structured-output', 'children'),
    dash.dependencies.Output('structured-argumentation-graph', 'data'),
    dash.dependencies.Input('create-argumentation-theory-button', 'n_clicks'),
    dash.dependencies.State('aspic-axioms', 'value'),
    dash.dependencies.State('aspic-ordinary-premises', 'value'),
    dash.dependencies.State('aspic-strict-rules', 'value'),
    dash.dependencies.State('aspic-defeasible-rules', 'value'),
    dash.dependencies.State('ordinary-prem-preferences', 'value'),
    dash.dependencies.State('defeasible-rule-preferences', 'value'),
    dash.dependencies.State('ordering-choice', 'value'),
    dash.dependencies.State('ordering-link', 'value'),
    dash.dependencies.Input('selected-argument-store-structured', 'data'),
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


@app.callback(
    dash.dependencies.Output('structured-evaluation', 'children'),
    dash.dependencies.Input('evaluate-structured-argumentation-theory-button', 'n_clicks'),
    dash.dependencies.State('aspic-axioms', 'value'),
    dash.dependencies.State('aspic-ordinary-premises', 'value'),
    dash.dependencies.State('aspic-strict-rules', 'value'),
    dash.dependencies.State('aspic-defeasible-rules', 'value'),
    dash.dependencies.State('ordinary-prem-preferences', 'value'),
    dash.dependencies.State('defeasible-rule-preferences', 'value'),
    dash.dependencies.State('ordering-choice', 'value'),
    dash.dependencies.State('ordering-link', 'value'),
    dash.dependencies.State('structured-evaluation-semantics', 'value'),
    dash.dependencies.State('structured-evaluation-strategy', 'value'),
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


@app.callback(
    dash.dependencies.Output('selected-argument-store-structured', 'data'),
    dash.dependencies.Input({'type': 'extension-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    dash.dependencies.State('selected-argument-store-structured', 'data'),
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


@app.callback(
    dash.dependencies.Output('structured-explanation', 'children'),
    dash.dependencies.Input('structured-explanation-button', 'n_clicks'),
    dash.dependencies.State('aspic-axioms', 'value'),
    dash.dependencies.State('aspic-ordinary-premises', 'value'),
    dash.dependencies.State('aspic-strict-rules', 'value'),
    dash.dependencies.State('aspic-defeasible-rules', 'value'),
    dash.dependencies.State('ordinary-prem-preferences', 'value'),
    dash.dependencies.State('defeasible-rule-preferences', 'value'),
    dash.dependencies.State('ordering-choice', 'value'),
    dash.dependencies.State('ordering-link', 'value'),
    dash.dependencies.State('structured-evaluation-semantics', 'value'),
    dash.dependencies.State('structured-explanation-function', 'value'),
    dash.dependencies.State('structured-explanation-type', 'value'),
    dash.dependencies.State('structured-explanation-strategy', 'value'),
    dash.dependencies.State('structured-explanation-form', 'value'),
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


@app.callback(
    dash.dependencies.Output('structured-argumentation-graph-output', 'children'),
    dash.dependencies.Output('structured-argumentation-graph-evaluation', 'children'),
    dash.dependencies.Output('structured-argumentation-graph-explanation', 'children'),
    dash.dependencies.Input('structured-argumentation-graph', 'selection'),
    dash.dependencies.Input('structured-argumentation-graph', 'data'),
    dash.dependencies.Input('aspic-axioms', 'value'),
    dash.dependencies.Input('aspic-ordinary-premises', 'value'),
    dash.dependencies.Input('aspic-strict-rules', 'value'),
    dash.dependencies.Input('aspic-defeasible-rules', 'value'),
    dash.dependencies.Input('ordinary-prem-preferences', 'value'),
    dash.dependencies.Input('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
    dash.dependencies.Input('ordering-link', 'value'),
    dash.dependencies.Input('structured-evaluation-semantics', 'value'),
    dash.dependencies.Input('structured-explanation-function', 'value'),
    dash.dependencies.Input('structured-explanation-type', 'value'),
    dash.dependencies.Input('structured-evaluation-strategy', 'value'),
    dash.dependencies.Input('structured-explanation-form', 'value'),
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


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
