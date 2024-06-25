import base64
import json
from typing import List, Dict

import dash
import visdcc
from dash import html, callback, Input, Output, State, ALL, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_interactive_graphviz

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.generators. \
    abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_from_aspartix_format_reader import \
    ArgumentationFrameworkFromASPARTIXFormatReader
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_from_iccma23_format_reader import \
    ArgumentationFrameworkFromICCMA23FormatReader
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_from_json_reader import \
    ArgumentationFrameworkFromJsonReader
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_from_trivial_graph_format_reader import \
    ArgumentationFrameworkFromTrivialGraphFormatReader
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_aspartix_format_writer import \
    ArgumentationFrameworkToASPARTIXFormatWriter
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_iccma23_format_writer import \
    ArgumentationFrameworkToICCMA23FormatWriter
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_json_writer import \
    ArgumentationFrameworkToJSONWriter
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_trivial_graph_format_writer import \
    ArgumentationFrameworkToTrivialGraphFormatWriter
from py_arg_visualisation.functions.explanations_functions. \
    explanation_function_options import \
    EXPLANATION_FUNCTION_OPTIONS
from py_arg_visualisation.functions.explanations_functions. \
    get_af_explanations import \
    get_argumentation_framework_explanations
from py_arg.abstract_argumentation.semantics.get_accepted_arguments import \
    get_accepted_arguments
from py_arg.abstract_argumentation.semantics. \
    get_argumentation_framework_extensions import \
    get_argumentation_framework_extensions
from py_arg_visualisation.functions.extensions_functions. \
    get_acceptance_strategy import get_acceptance_strategy
from py_arg_visualisation.functions.graph_data_functions.get_af_dot_string \
    import generate_plain_dot_string, generate_dot_string
from py_arg_visualisation.functions.graph_data_functions. \
    get_af_graph_data import get_argumentation_framework_graph_data
from py_arg_visualisation.functions.import_functions. \
    read_argumentation_framework_functions import \
    read_argumentation_framework

dash.register_page(__name__, name='Visualise AF', title='Visualise AF')


# Create layout elements and compose them into the layout for this page.

def get_abstract_setting_specification_div():
    return html.Div(children=[
        dcc.Store(id='selected-argument-store-abstract'),
        dbc.Col([
            dbc.Row([dbc.Col(dbc.Button(
                'Generate random',
                id='generate-random-af-button', n_clicks=0,
                className='w-100')),
                dbc.Col(dcc.Upload(dbc.Button(
                    'Open existing AF', className='w-100'),
                    id='upload-af'))
            ], className='mt-2'),
            dbc.Row([
                dbc.Col([
                    html.B('Arguments'),
                    dbc.Textarea(
                        id='abstract-arguments',
                        placeholder='Add one argument per line. '
                                    'For example:\n A\n B\n C',
                        value='', style={'height': '300px'})
                ]),
                dbc.Col([
                    html.B('Attacks'),
                    dbc.Textarea(
                        id='abstract-attacks',
                        placeholder='Add one attack per line. '
                                    'For example: \n (A,B) \n (A,C) \n (C,B)',
                        value='', style={'height': '300px'}),
                ])
            ], className='mt-2'),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText('Filename'),
                    dbc.Input(value='edited_af', id='21-af-filename'),
                    dbc.InputGroupText('.'),
                    dbc.Select(
                        options=[{'label': extension, 'value': extension}
                                 for extension in ['JSON', 'TGF', 'APX',
                                                   'ICCMA23']],
                        value='JSON', id='21-af-extension'),
                    dbc.Button('Download', id='21-af-download-button'),
                ], className='mt-2'),
                dcc.Download(id='21-af-download')
            ])
        ])
    ])


def get_abstract_evaluation_div():
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.B('Semantics')),
                dbc.Col(dbc.Select(options=[
                    {'label': 'Admissible', 'value': 'Admissible'},
                    {'label': 'Complete', 'value': 'Complete'},
                    {'label': 'Grounded', 'value': 'Grounded'},
                    {'label': 'Preferred', 'value': 'Preferred'},
                    {'label': 'Ideal', 'value': 'Ideal'},
                    {'label': 'Stage', 'value': 'Stage'},
                    {'label': 'Stable', 'value': 'Stable'},
                    {'label': 'Semi-stable', 'value': 'SemiStable'},
                    {'label': 'Eager', 'value': 'Eager'},
                    {'label': 'Conflict-free', 'value': 'ConflictFree'},
                    {'label': 'Naive', 'value': 'Naive'}
                ], value='Complete', id='abstract-evaluation-semantics')),
            ]),
            dbc.Row(id='21-abstract-evaluation-semantics'),
            dbc.Row([
                dbc.Col(html.B('Evaluation strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ], value='Credulous', id='abstract-evaluation-strategy')),
            ]),
            dbc.Row(id='21-abstract-evaluation-accepted')
        ]),
    ])


def get_abstract_explanation_div():
    return html.Div([
        dbc.Row([
            dbc.Col(html.B('Type')),
            dbc.Col(dbc.Select(
                options=[{'label': 'Acceptance', 'value': 'Acceptance'},
                         {'label': 'Non-Acceptance',
                          'value': 'NonAcceptance'}],
                value='Acceptance', id='abstract-explanation-type'))]),
        dbc.Row([
            dbc.Col(html.B('Explanation function')),
            dbc.Col(dbc.Select(id='abstract-explanation-function'))
        ]),
        dbc.Row(id='abstract-explanation')
    ])


left_column = dbc.Col(
    dbc.Accordion([
        dbc.AccordionItem(get_abstract_setting_specification_div(),
                          title='Abstract Argumentation Framework',
                          item_id='ArgumentationFramework'),
        dbc.AccordionItem(get_abstract_evaluation_div(),
                          title='Evaluation', item_id='Evaluation'),
        dbc.AccordionItem(get_abstract_explanation_div(),
                          title='Explanation', item_id='Explanation')
    ], id='abstract-evaluation-accordion')
)

right_column = dbc.Col([
    dbc.Row([
        dbc.Card(
            dcc.Tabs([
                dcc.Tab(label='Default visualisation', children=[
                    visdcc.Network(
                        data={'nodes': [], 'edges': []},
                        id='abstract-argumentation-graph',
                        options={'height': '545px'}
                    ),
                ]),
                dcc.Tab(label='Layered visualisation', children=[
                    html.Div(style={'height': '5px'}),
                    dbc.Row([
                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col(html.B('Layout'), width=5),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {'label': 'Left to right', 'value': 'LR'},
                                                {'label': 'Right to left', 'value': 'RL'},
                                                {'label': 'Bottom to top', 'value': 'BT'},
                                                {'label': 'Top to bottom', 'value': 'TB'}
                                            ],
                                            value='BT',
                                            id='21-abstract-graph-layout',
                                        ),
                                    ),
                                ]),
                                html.Div(style={'height': '5px'}),
                                dbc.Row([
                                    dbc.Col(html.B('Rank'), width=5),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {'label': 'No Rank', 'value': 'NR'},
                                                {'label': 'Min Rank', 'value': 'MR'},
                                                {'label': 'All Rank', 'value': 'AR'},
                                            ],
                                            value='NR',
                                            id='21-abstract-graph-rank',
                                        ),
                                    ),
                                ]),
                                html.Div(style={'height': '5px'}),
                                dbc.Row([
                                    dbc.Col(html.B('Edge Constraint (False)'), width=5),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=[
                                                {'label': 'Defeated ⟶ Defeated', 'value': 'DD'},
                                                {'label': 'Undecided ⟶ Defeated', 'value': 'UD'},
                                                {'label': 'Defeated ⟶ Undecided', 'value': 'DU'},
                                                {'label': 'Undecided ⟶ Undecided', 'value': 'UU'},
                                                {'label': 'Against the Wind', 'value': 'AW'},
                                            ],
                                            multi=True,
                                            id='21-abstract-graph-edge-con',
                                        ),
                                    ),
                                ]),
                                html.Div(style={'height': '5px'}),
                                dbc.Row([
                                    dbc.Col(html.B('Remove Edges'), width=5),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=[
                                                {'label': 'Defeated ⟶ Defeated', 'value': 'DD'},
                                                {'label': 'Undecided ⟶ Defeated', 'value': 'UD'},
                                                {'label': 'Defeated ⟶ Undecided', 'value': 'DU'},
                                                {'label': 'Undecided ⟶ Undecided', 'value': 'UU'},
                                                {'label': 'Against the Wind', 'value': 'AW'},
                                            ],
                                            multi=True,
                                            id='21-abstract-graph-edge-rm',
                                        ),
                                    ),
                                ]),
                            ],
                            width=9,
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    'Download dot', 
                                    id='21-dot-download-button',
                                    style={
                                        'width': '95px',
                                        'margin': '10px auto',
                                    },
                                ),
                                dcc.Download(id="21-dot-download"),
                            ],
                            className="d-flex justify-content-center align-items-center",  
                            width=3,
                        ),
                    ]),
                    html.Div([
                        dash_interactive_graphviz.DashInteractiveGraphviz(
                            id='explanation-graph',
                            persisted_props={'engine': "neato"},
                            style={'height': '550px', 'max-width': '98%', 'overflow': 'hidden'},
                        ),
                    ], style={'height': '550px', 'max-width': '98%', 'overflow': 'hidden'}),
                ]),
            ]),
        ),
    ]),
])

layout_abstract = dbc.Row([left_column, right_column])
layout = html.Div([html.H1(
    'Visualisation of abstract argumentation frameworks'), layout_abstract])


@callback(
    Output('abstract-arguments', 'value'),
    Output('abstract-attacks', 'value'),
    Input('generate-random-af-button', 'n_clicks'),
    Input('upload-af', 'contents'),
    State('upload-af', 'filename'),
)
def generate_abstract_argumentation_framework(
        _nr_of_clicks_random: int, af_content: str, af_filename: str):
    """
    Generate a random AF after clicking the button and put the result in the
    text box.
    """
    if dash.callback_context.triggered_id == 'generate-random-af-button':
        random_af = \
            AbstractArgumentationFrameworkGenerator(8, 8, True).generate()
        abstract_arguments_value = '\n'.join((str(arg)
                                              for arg in random_af.arguments))
        abstract_attacks_value = '\n'.join((f'({str(defeat.from_argument)},'
                                            f'{str(defeat.to_argument)})'
                                            for defeat in random_af.defeats))
        return abstract_arguments_value, abstract_attacks_value
    elif dash.callback_context.triggered_id == 'upload-af':
        content_type, content_str = af_content.split(',')
        decoded = base64.b64decode(content_str)

        name = af_filename.split('.')[0]
        if af_filename.upper().endswith('.JSON'):
            opened_af = ArgumentationFrameworkFromJsonReader().from_json(
                json.loads(decoded))
        elif af_filename.upper().endswith('.TGF'):
            opened_af = ArgumentationFrameworkFromTrivialGraphFormatReader. \
                from_tgf(decoded.decode(), name)
        elif af_filename.upper().endswith('.APX'):
            opened_af = ArgumentationFrameworkFromASPARTIXFormatReader. \
                from_apx(decoded.decode(), name)
        elif af_filename.upper().endswith('.ICCMA23'):
            opened_af = ArgumentationFrameworkFromICCMA23FormatReader. \
                from_iccma23(decoded.decode(), name)
        else:
            raise NotImplementedError('This file format is currently not '
                                      'supported.')

        abstract_arguments_value = '\n'.join((str(arg)
                                              for arg in opened_af.arguments))
        abstract_attacks_value = '\n'.join((f'({str(defeat.from_argument)},'
                                            f'{str(defeat.to_argument)})'
                                            for defeat in opened_af.defeats))
        return abstract_arguments_value, abstract_attacks_value
    return '', ''


@callback(
    Output('21-dot-download', 'data'),
    Output('abstract-argumentation-graph', 'data'),
    Output('explanation-graph', 'dot_source'),
    Input('21-dot-download-button', 'n_clicks'),
    Input('abstract-arguments', 'value'),
    Input('abstract-attacks', 'value'),
    Input('selected-argument-store-abstract', 'data'),
    Input('color-blind-mode', 'on'),
    Input('21-abstract-graph-layout', 'value'),
    Input('21-abstract-graph-rank', 'value'),
    Input('21-abstract-graph-edge-con', 'value'),
    Input('21-abstract-graph-edge-rm', 'value'),
    Input('abstract-evaluation-accordion', 'active_item'),
    prevent_initial_call=True
)
def create_abstract_argumentation_framework(
        _nr_clicks: int, arguments: str, attacks: str, selected_arguments: Dict[str, List[str]],
        color_blind_mode: bool, dot_layout: str, dot_rank:str, dot_con:List[str], 
        dot_rm_edge: List[str], active_item: str):
    """
    Send the AF data to the graph for plotting.
    """

    # Read the argumentation framework; in case of an error, display nothing.
    try:
        arg_framework = read_argumentation_framework(arguments, attacks)
    except ValueError:
        arg_framework = AbstractArgumentationFramework()

    # Do not display colors if the argumentation framework tab is open.
    if active_item == 'ArgumentationFramework':
        selected_arguments = None

    data = get_argumentation_framework_graph_data(
        arg_framework, selected_arguments, color_blind_mode)
    if selected_arguments:
        dot_source = generate_dot_string(
            arg_framework, selected_arguments, color_blind_mode, dot_layout, dot_rank, dot_con, dot_rm_edge)
    else:
        dot_source = generate_plain_dot_string(arg_framework, dot_layout)
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "21-dot-download-button" in changed_id:
        return dict(content=dot_source, filename="pyarg_output.dot"), data, dot_source
    else:
        return None, data, dot_source


@callback(
    Output('21-af-download', 'data'),
    Input('21-af-download-button', 'n_clicks'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    State('21-af-filename', 'value'),
    State('21-af-extension', 'value'),
    prevent_initial_call=True,
)
def download_generated_abstract_argumentation_framework(
        _nr_clicks: int, arguments_text: str, defeats_text: str, filename: str,
        extension: str):
    argumentation_framework = read_argumentation_framework(arguments_text,
                                                           defeats_text)

    if extension == 'JSON':
        argumentation_framework_json = \
            ArgumentationFrameworkToJSONWriter().to_dict(
                argumentation_framework)
        argumentation_framework_str = json.dumps(argumentation_framework_json)
    elif extension == 'TGF':
        argumentation_framework_str = \
            ArgumentationFrameworkToTrivialGraphFormatWriter.write_to_str(
                argumentation_framework)
    elif extension == 'APX':
        argumentation_framework_str = \
            ArgumentationFrameworkToASPARTIXFormatWriter.write_to_str(
                argumentation_framework)
    elif extension == 'ICCMA23':
        argumentation_framework_str = \
            ArgumentationFrameworkToICCMA23FormatWriter.write_to_str(
                argumentation_framework)
    else:
        raise NotImplementedError

    return {'content': argumentation_framework_str,
            'filename': filename + '.' + extension}


@callback(
    Output('21-abstract-evaluation-semantics', 'children'),
    Output('21-abstract-evaluation-accepted', 'children'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    Input('abstract-evaluation-accordion', 'active_item'),
    Input('abstract-evaluation-semantics', 'value'),
    Input('abstract-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_abstract_argumentation_framework(arguments: str, attacks: str,
                                              active_item: str,
                                              semantics: str, strategy: str):
    if active_item != 'Evaluation':
        raise PreventUpdate

    # Read the abstract argumentation framework.
    arg_framework = read_argumentation_framework(arguments, attacks)

    # Compute the extensions and put them in a list of sets.
    frozen_extensions = get_argumentation_framework_extensions(arg_framework,
                                                               semantics)
    extensions = [set(frozen_extension)
                  for frozen_extension in frozen_extensions]

    # Make a button for each extension.
    extension_buttons = []
    for extension in sorted(extensions):
        out_arguments = {attacked for attacked in arg_framework.arguments
                         if any(argument in arg_framework.
                                get_incoming_defeat_arguments(attacked)
                                for argument in extension)}
        undecided_arguments = {argument for argument in arg_framework.arguments
                               if argument not in extension and
                               argument not in out_arguments}
        extension_readable_str = \
            '{' + ', '.join(argument.name
                            for argument in sorted(extension)) + '}'
        extension_in_str = \
            '+'.join(argument.name for argument in sorted(extension))
        extension_out_str = \
            '+'.join(argument.name for argument in sorted(out_arguments))
        extension_undecided_str = \
            '+'.join(argument.name for argument in sorted(undecided_arguments))
        extension_long_str = \
            '|'.join([extension_in_str, extension_undecided_str,
                      extension_out_str])
        extension_buttons.append(
            dbc.Button([extension_readable_str], color='secondary',
                       id={'type': 'extension-button-abstract',
                           'index': extension_long_str}))

    # Based on the extensions, get the acceptance status of arguments.
    acceptance_strategy = get_acceptance_strategy(strategy)
    accepted_arguments = get_accepted_arguments(
        frozen_extensions, acceptance_strategy)

    # Make a button for each accepted argument.
    accepted_argument_buttons = [
        dbc.Button(argument.name, color='secondary',
                   id={'type': 'argument-button-abstract',
                       'index': argument.name})
        for argument in sorted(accepted_arguments)]

    semantics_div = html.Div([
        html.B('The extension(s):'),
        html.Br(),
        html.I('Click on the extension buttons to '
               'display the corresponding extension '
               'in the graph.'),
        html.Div(extension_buttons),
        html.Br()
    ])
    accepted_div = html.Div([
        html.B('The accepted argument(s):'),
        html.Br(),
        html.I('Click on the accepted argument buttons to '
               'display the corresponding argument '
               'in the graph.'),
        html.Div(accepted_argument_buttons),
    ])

    return semantics_div, accepted_div


@callback(
    Output('selected-argument-store-abstract', 'data'),
    Input({'type': 'extension-button-abstract', 'index': ALL}, 'n_clicks'),
    Input({'type': 'argument-button-abstract', 'index': ALL}, 'n_clicks'),
    Input('abstract-arguments', 'value'),
    Input('abstract-attacks', 'value'),
)
def mark_extension_or_argument_in_graph(_nr_of_clicks_extension_values,
                                        _nr_of_clicks_argument_values,
                                        _arguments, _attacks):
    # Remove stored selected arguments after any updates in arguments/attacks.
    if dash.ctx.triggered_id in ['abstract-arguments', 'abstract-attacks']:
        return []

    # Find the triggered button.
    button_clicked_id = \
        dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    # No triggered button, keep old selection.
    if button_clicked_id == '':
        return []

    # Update selected argument based on the clicked button.
    button_clicked_id_content = json.loads(button_clicked_id)
    button_clicked_id_type = button_clicked_id_content['type']
    button_clicked_id_index = button_clicked_id_content['index']
    if button_clicked_id_type == 'extension-button-abstract':
        in_part, undecided_part, out_part = \
            button_clicked_id_index.split('|', 3)
        return {'green': in_part.split('+'),
                'yellow': undecided_part.split('+'),
                'red': out_part.split('+')}
    elif button_clicked_id_type == 'argument-button-abstract':
        return {'blue': [button_clicked_id_index]}

    return []


@callback(
    Output('abstract-explanation-function', 'options'),
    Output('abstract-explanation-function', 'value'),
    [Input('abstract-explanation-type', 'value')]
)
def setting_choice(choice: str):
    return EXPLANATION_FUNCTION_OPTIONS[choice], \
        EXPLANATION_FUNCTION_OPTIONS[choice][0]['value']


@callback(
    Output('abstract-explanation', 'children'),
    Input('abstract-evaluation-accordion', 'active_item'),
    State('abstract-arguments', 'value'),
    State('abstract-attacks', 'value'),
    State('abstract-evaluation-semantics', 'value'),
    Input('abstract-explanation-function', 'value'),
    Input('abstract-explanation-type', 'value'),
    State('abstract-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def derive_explanations_abstract_argumentation_framework(
        active_item, arguments: str, attacks: str, semantics: str,
        explanation_function: str, explanation_type: str,
        explanation_strategy: str):
    if active_item != 'Explanation':
        raise PreventUpdate

    # Compute the explanations based on the input.
    arg_framework = read_argumentation_framework(arguments, attacks)
    frozen_extensions = get_argumentation_framework_extensions(arg_framework,
                                                               semantics)
    extensions = [set(frozen_extension)
                  for frozen_extension in frozen_extensions]
    acceptance_strategy = get_acceptance_strategy(explanation_strategy)
    accepted_arguments = get_accepted_arguments(
        frozen_extensions, acceptance_strategy)
    explanations = get_argumentation_framework_explanations(
        arg_framework, extensions, accepted_arguments,
        explanation_function, explanation_type)

    # Print the explanations for each of the arguments.
    return html.Div([html.Div(html.B('Explanation(s) by argument:'))] +
                    [html.Div([
                        html.B(explanation_key),
                        html.Ul([html.Li(str(explanation_value).replace(
                            'set()', '{}'))
                            for explanation_value in explanation_values])])
                        for explanation_key, explanation_values in
                        explanations.items()])
