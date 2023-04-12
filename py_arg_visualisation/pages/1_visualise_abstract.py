import json
from typing import List

import dash
from dash import html, callback, Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg_visualisation.functions.explanations_functions.explanation_function_options import \
    EXPLANATION_FUNCTION_OPTIONS
from py_arg_visualisation.functions.explanations_functions.get_af_explanations import \
    get_argumentation_framework_explanations
from py_arg_visualisation.functions.extensions_functions.get_accepted_arguments import get_accepted_arguments
from py_arg_visualisation.functions.extensions_functions.get_af_extensions import get_argumentation_framework_extensions
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data
from py_arg_visualisation.functions.import_functions.read_argumentation_framework_functions import \
    read_argumentation_framework
from py_arg_visualisation.layout_elements.abstract_argumentation_layout_elements import \
    get_abstract_setting_specification_div, get_abstract_evaluation_div, get_abstract_explanation_div, \
    get_abstract_layout

dash.register_page(__name__, name='Visualise AF', title='Visualise AF')

# Create layout elements and compose them into the layout for this page.
abstract_setting = get_abstract_setting_specification_div()
abstract_evaluation = get_abstract_evaluation_div()
abstract_explanation = get_abstract_explanation_div()
layout = get_abstract_layout(abstract_evaluation, abstract_explanation, abstract_setting)


@callback(
    Output('abstract-arguments', 'value'),
    Output('abstract-attacks', 'value'),
    Input('generate-random-af-button', 'n_clicks')
)
def generate_abstract_argumentation_framework(nr_of_clicks: int):
    """
    Generate a random AF after clicking the button and put the result in the text box.
    """
    if nr_of_clicks > 0:
        random_af = AbstractArgumentationFrameworkGenerator(8, 8, True).generate()
        abstract_arguments_value = '\n'.join((str(arg) for arg in random_af.arguments))
        abstract_attacks_value = '\n'.join((f'({str(defeat.from_argument)},{str(defeat.to_argument)})'
                                            for defeat in random_af.defeats))
        return abstract_arguments_value, abstract_attacks_value
    return '', ''


@callback(
    Output('abstract-argumentation-graph', 'data'),
    Input('create-argumentation-framework-button', 'n_clicks'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    Input('selected-argument-store-abstract', 'data'),
    prevent_initial_call=True
)
def create_abstract_argumentation_framework(_nr_of_clicks: int, arguments: str, attacks: str,
                                            selected_arguments: List[str]):
    """
    Send the AF data to the graph for plotting.
    """
    arg_framework = read_argumentation_framework(arguments, attacks)
    data = get_argumentation_framework_graph_data(arg_framework, selected_arguments)
    return data


@callback(
    Output('abstract-evaluation', 'children'),
    Input('evaluate-argumentation-framework-button', 'n_clicks'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    State('abstract-evaluation-semantics', 'value'),
    State('abstract-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_abstract_argumentation_framework(_nr_of_clicks: int, arguments: str, attacks: str, semantics: str,
                                              strategy: str):
    # Read the abstract argumentation framework.
    arg_framework = read_argumentation_framework(arguments, attacks)

    # Compute the extensions and put them in a list of sets.
    frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]

    # Make a button for each extension.
    extension_buttons = []
    for extension in sorted(extensions):
        extension_readable_str = '{' + ', '.join(argument.name for argument in sorted(extension)) + '}'
        extension_long_str = '+'.join(argument.name for argument in sorted(extension))
        extension_buttons.append(dbc.Button([extension_readable_str], color='secondary',
                                            id={'type': 'extension-button-abstract', 'index': extension_long_str}))

    # Based on the extensions, get the acceptance status of arguments.
    accepted_arguments = get_accepted_arguments(extensions, strategy)

    # Make a button for each accepted argument.
    accepted_argument_buttons = [dbc.Button(argument.name, color='secondary', id={'type': 'argument-button-abstract',
                                                                                  'index': argument.name})
                                 for argument in sorted(accepted_arguments)]

    return html.Div([html.B('The extension(s):'), html.Div(extension_buttons),
                     html.B('The accepted argument(s):'), html.Div(accepted_argument_buttons),
                     html.P('Click on the extension/argument buttons to display the corresponding argument(s) '
                            'in the graph.')])


@callback(
    Output('selected-argument-store-abstract', 'data'),
    Input({'type': 'extension-button-abstract', 'index': ALL}, 'n_clicks'),
    Input({'type': 'argument-button-abstract', 'index': ALL}, 'n_clicks'),
    State('selected-argument-store-abstract', 'data'),
)
def mark_extension_or_argument_in_graph(_nr_of_clicks_extension_values, _nr_of_clicks_argument_values,
                                        old_selected_data: List[str]):
    button_clicked_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_clicked_id == '':
        return old_selected_data
    button_clicked_id_content = json.loads(button_clicked_id)
    button_clicked_id_type = button_clicked_id_content['type']
    button_clicked_id_index = button_clicked_id_content['index']
    if button_clicked_id_type == 'extension-button-abstract':
        return button_clicked_id_index.split('+')
    elif button_clicked_id_type == 'argument-button-abstract':
        return [button_clicked_id_index]
    return []


@callback(
    Output('abstract-explanation-function', 'options'),
    [Input('abstract-explanation-type', 'value')]
)
def setting_choice(choice: str):
    return [{'label': i, 'value': i} for i in EXPLANATION_FUNCTION_OPTIONS[choice]]


@callback(
    Output('abstract-explanation', 'children'),
    Input('abstract-explanation-button', 'n_clicks'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    State('abstract-evaluation-semantics', 'value'),
    State('abstract-explanation-function', 'value'),
    State('abstract-explanation-type', 'value'),
    State('abstract-explanation-strategy', 'value'),
    prevent_initial_call=True
)
def derive_explanations_abstract_argumentation_framework(_nr_of_clicks: int, arguments: str, attacks: str,
                                                         semantics: str, explanation_function: str,
                                                         explanation_type: str, explanation_strategy: str):
    # Compute the explanations based on the input.
    arg_framework = read_argumentation_framework(arguments, attacks)
    frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
    accepted_arguments = get_accepted_arguments(extensions, explanation_strategy)
    explanations = get_argumentation_framework_explanations(arg_framework, extensions, accepted_arguments,
                                                            explanation_function, explanation_type)

    # Print the explanations for each of the arguments.
    return html.Div([html.B('The explanation(s):')] +
                    [html.Div([
                        html.B(explanation_key),
                        html.Ul([html.Li(str(explanation_value)) for explanation_value in explanation_values])])
                     for explanation_key, explanation_values in explanations.items()])


@callback(
    Output('abstract-argumentation-graph-evaluation', 'children'),
    Output('abstract-argumentation-graph-explanation', 'children'),
    Input('abstract-argumentation-graph', 'selection'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    State('abstract-evaluation-semantics', 'value'),
    State('abstract-evaluation-strategy', 'value'),
    State('abstract-explanation-function', 'value'),
    State('abstract-explanation-type', 'value'),
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
            [html.B('The selected argument:'), html.H6('{}'.format(str(argument)))])
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
                        skeptical_explanation = get_argumentation_framework_explanations(arg_framework, extensions,
                                                                                         skeptically_accepted_arguments,
                                                                                         function, explanation_type)
                        credulous_explanation = get_argumentation_framework_explanations(arg_framework, extensions,
                                                                                         credulously_accepted_arguments,
                                                                                         function, explanation_type)
                        explanation_output = html.Div([html.B(
                            'The skeptical acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(
                                str(skeptical_explanation.get(str(argument))).replace('set()', '{}'))), html.B(
                                'The credulous acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(
                                str(credulous_explanation.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        explanation_output = html.Div(
                            [html.B('Error', className='error'),
                             'There is no non-acceptance explanation for argument {}, since it is '
                             'skeptically accepted.'.format(argument)])
                elif credulously_accepted:
                    output_accept += str(argument) + ' is credulously but not skeptically accepted.'
                    if function is not None and explanation_type == 'Acceptance':
                        credulous_explanation = get_argumentation_framework_explanations(arg_framework, extensions,
                                                                                         credulously_accepted_arguments,
                                                                                         function, explanation_type)
                        explanation_output = html.Div(
                            [html.B('The credulous acceptance explanation for {}:'.format(str(argument))),
                             html.H6('\n {}'.format(
                                 str(credulous_explanation.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and explanation_type == 'NonAcceptance':
                        skeptical_explanation = get_argumentation_framework_explanations(arg_framework, extensions,
                                                                                         skeptically_accepted_arguments,
                                                                                         function, explanation_type)
                        explanation_output = html.Div(
                            [html.B('The not skeptical acceptance explanation for {}:'.format(str(argument))),
                             html.H6('\n {}'.format(
                                 str(skeptical_explanation.get(str(argument))).replace('set()', '{}')))])
                elif not skeptically_accepted and not credulously_accepted:
                    output_accept += str(argument) + ' is neither  credulously nor skeptically accepted.'
                    if function is not None and explanation_type == 'NonAcceptance':
                        skeptical_explanation = get_argumentation_framework_explanations(arg_framework, extensions,
                                                                                         skeptically_accepted_arguments,
                                                                                         function, explanation_type)
                        credulous_explanation = get_argumentation_framework_explanations(arg_framework, extensions,
                                                                                         credulously_accepted_arguments,
                                                                                         function, explanation_type)
                        explanation_output = html.Div([html.B(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(skeptical_explanation.get(str(argument))).replace('set()', '{}'))), html.B(
                                'The not credulous acceptance explanation for {}:'.format(str(argument))),
                            html.H6('\n {}'.format(str(credulous_explanation.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and explanation_type == 'Acceptance':
                        explanation_output = html.Div(
                            [html.B('Error', className='error'),
                             'There is no acceptance explanation for argument {}, since it is not '
                             'credulously accepted.'.format(argument)])
            output_evaluation = html.Div(
                [html.B('The extensions with argument {}:'.format(str(argument))),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_evaluation, explanation_output
    raise PreventUpdate
