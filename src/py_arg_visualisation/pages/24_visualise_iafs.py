import base64
import json

import dash
import visdcc
from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from py_arg.incomplete_argumentation_frameworks.classes. \
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg.incomplete_argumentation_frameworks.generators.\
    random_iaf_generator import IAFGenerator
from py_arg.incomplete_argumentation_frameworks.import_export.\
    iaf_from_json_reader import IAFFromJsonReader
from py_arg.incomplete_argumentation_frameworks.import_export.\
    iaf_to_json_writer import IAFToJSONWriter
from py_arg.incomplete_argumentation_frameworks.semantics.\
    grounded_relevance import GroundedRelevanceWithPreprocessingSolver
from py_arg.incomplete_argumentation_frameworks.semantics.\
    grounded_stability import GroundedStabilitySolver
from py_arg_visualisation.functions.graph_data_functions.get_iaf_graph_data \
    import get_iaf_graph_data
from py_arg_visualisation.functions.import_functions.read_iaf_functions \
    import read_incomplete_argumentation_framework

dash.register_page(__name__, name='Visualise IAF', title='Visualise IAF')


def get_abstract_setting_specification_div():
    return html.Div(children=[
        dbc.Col([
            dbc.Row([dbc.Col(dbc.Button(
                'Generate random',
                id='24-generate-random-af-button', n_clicks=0,
                className='w-100')),
                dbc.Col(dcc.Upload(dbc.Button(
                    'Open existing IAF', className='w-100'),
                    id='24-upload-iaf'))
            ], className='mt-2'),
            dbc.Row([
                dbc.Col([
                    html.B('Certain arguments'),
                    dbc.Textarea(
                        id='24-certain-arguments',
                        placeholder='Add one argument per line. '
                                    'For example:\n A\n B',
                        value='', style={'height': '150px'})
                ]),
                dbc.Col([
                    html.B('Certain attacks'),
                    dbc.Textarea(
                        id='24-certain-attacks',
                        placeholder='Add one attack per line. '
                                    'For example: \n (A,B) \n (A,C)',
                        value='', style={'height': '150px'}),
                ])
            ], className='mt-2'),
            dbc.Row([
                dbc.Col([
                    html.B('Uncertain arguments'),
                    dbc.Textarea(
                        id='24-uncertain-arguments',
                        placeholder='Add one argument per line. '
                                    'For example:\n C',
                        value='', style={'height': '150px'})
                ]),
                dbc.Col([
                    html.B('Uncertain attacks'),
                    dbc.Textarea(
                        id='24-uncertain-attacks',
                        placeholder='Add one attack per line. '
                                    'For example: \n (C,B)',
                        value='', style={'height': '150px'}),
                ])
            ], className='mt-2'),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText('Filename'),
                    dbc.Input(value='edited_iaf', id='24-iaf-filename'),
                    dbc.InputGroupText('.'),
                    dbc.Select(
                        options=[{'label': extension, 'value': extension}
                                 for extension in ['JSON']],
                        value='JSON', id='24-iaf-extension'),
                    dbc.Button('Download', id='24-iaf-download-button'),
                ], className='mt-2'),
                dcc.Download(id='24-iaf-download')
            ])
        ])
    ])


def get_abstract_evaluation_div():
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.B('Semantics')),
                dbc.Col(dbc.Select(options=[
                    {'label': 'Complete', 'value': 'Complete'},
                    {'label': 'Grounded', 'value': 'Grounded'}
                ], value='Grounded', id='24-iaf-evaluation-semantics')),
            ]),

            dbc.Row([
                dbc.Col(html.B('Evaluation strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ], value='Credulous', id='24-iaf-evaluation-strategy'))
            ]),

            dbc.Row([
                dbc.Col(html.B('Topic argument')),
                dbc.Col(dbc.Select(id='24-topic-argument'))
            ]),
            dbc.Row(dbc.Col(html.Div(id='24-iaf-evaluation')))
        ]),
    ])


left_column = dbc.Col(
    dbc.Accordion([
        dbc.AccordionItem(get_abstract_setting_specification_div(),
                          title='Incomplete Argumentation Framework',
                          item_id='IAF'),
        dbc.AccordionItem(get_abstract_evaluation_div(),
                          title='Evaluation', item_id='Evaluation'),
    ], id='24-iaf-evaluation-accordion')
)

right_column = dbc.Col([
    dbc.Row([
        dbc.Card(
            visdcc.Network(data={'nodes': [], 'edges': []},
                           id='24-iaf-argumentation-graph',
                           options={'height': '500px'}))
    ])])

layout_iaf = dbc.Row([left_column, right_column])
layout = html.Div([html.H1(
    'Visualisation of incomplete argumentation frameworks'), layout_iaf])


@callback(
    Output('24-topic-argument', 'options'),
    Output('24-topic-argument', 'value'),
    Input('24-certain-arguments', 'value'),
    State('24-certain-attacks', 'value'),
    State('24-uncertain-arguments', 'value'),
    State('24-uncertain-attacks', 'value'),
    prevent_initial_call=True
)
def update_topic(
        certain_arguments: str, certain_attacks: str,
        uncertain_arguments: str, uncertain_attacks: str):
    """
    Send the IAF data to the graph for plotting.
    """

    # Read the argumentation framework; in case of an error, display nothing.
    try:
        iaf = read_incomplete_argumentation_framework(
            certain_arguments, certain_attacks,
            uncertain_arguments, uncertain_attacks)
    except ValueError:
        iaf = IncompleteArgumentationFramework()

    if not iaf.arguments:
        return [], None

    topic_value = iaf.arguments[next(iter(iaf.arguments))].name
    topic_options = [{'label': argument.name, 'value': argument.name}
                     for argument in sorted(iaf.arguments.values())]
    return topic_options, topic_value


@callback(
    Output('24-iaf-argumentation-graph', 'data'),
    Output('24-iaf-evaluation', 'children'),
    Input('24-certain-arguments', 'value'),
    Input('24-certain-attacks', 'value'),
    Input('24-uncertain-arguments', 'value'),
    Input('24-uncertain-attacks', 'value'),
    Input('color-blind-mode', 'on'),
    Input('24-iaf-evaluation-accordion', 'active_item'),
    Input('24-iaf-evaluation-semantics', 'value'),
    Input('24-iaf-evaluation-strategy', 'value'),
    Input('24-topic-argument', 'value'),
    prevent_initial_call=True
)
def display_iaf(
        certain_arguments: str, certain_attacks: str,
        uncertain_arguments: str, uncertain_attacks: str,
        color_blind_mode: bool, active_item: str,
        semantics: str, strategy: str, topic: str):
    """
    Send the IAF data to the graph for plotting.
    """

    # Read the argumentation framework; in case of an error, display nothing.
    try:
        iaf = read_incomplete_argumentation_framework(
            certain_arguments, certain_attacks,
            uncertain_arguments, uncertain_attacks)
    except ValueError:
        iaf = IncompleteArgumentationFramework()

    # If we are in the IAF tab, display the graph without colors.
    if active_item == 'IAF':
        return get_iaf_graph_data(iaf, None, [], [], color_blind_mode), ''

    # Otherwise, we are in the evaluation tab.
    if semantics == 'Grounded':
        # Compute stability status of the topic.
        stability_solver = GroundedStabilitySolver()
        stability_solver.enumerate_stable_arguments(iaf, topic)
        stability_result = stability_solver.get_result()

        # If the topic is stable, just show this result.
        if stability_result:
            graph_data = get_iaf_graph_data(
                iaf, topic, [], [], color_blind_mode)
            relevance_text = [html.P(stability_result)]
            return graph_data, relevance_text

        # Otherwise compute all relevant updates.
        relevance_solver = GroundedRelevanceWithPreprocessingSolver()
        relevance_solver.enumerate_grounded_relevant_updates(iaf, topic)
        relevant_updates = relevance_solver.get_printable_result()
        selected_arguments, selected_attacks = \
            relevance_solver.get_relevant_args_and_atts()

        # Show relevant updates.
        graph_data = get_iaf_graph_data(
            iaf, topic, selected_arguments, selected_attacks, color_blind_mode)
        relevance_text = [html.P(f'{topic} is unstable.'),
                          html.Ul([html.Li(relevant_item)
                                   for relevant_item in relevant_updates])]
        return graph_data, relevance_text

    return get_iaf_graph_data(iaf, None, [], [], color_blind_mode), \
        'This semantics has no algorithm yet.'


@callback(
    Output('24-iaf-download', 'data'),
    Input('24-iaf-download-button', 'n_clicks'),
    State('24-certain-arguments', 'value'),
    State('24-certain-attacks', 'value'),
    State('24-uncertain-arguments', 'value'),
    State('24-uncertain-attacks', 'value'),
    State('24-iaf-filename', 'value'),
    State('24-iaf-extension', 'value'),
    prevent_initial_call=True,
)
def download_iaf(
        _nr_clicks: int, arguments_text: str, defeats_text: str,
        uncertain_arguments_text: str, uncertain_defeats_text: str,
        filename: str,
        extension: str):
    try:
        iaf = read_incomplete_argumentation_framework(
            arguments_text, defeats_text,
            uncertain_arguments_text, uncertain_defeats_text)
    except ValueError:
        iaf = IncompleteArgumentationFramework()

    if extension == 'JSON':
        argumentation_framework_json = \
            IAFToJSONWriter().to_dict(iaf)
        argumentation_framework_str = json.dumps(argumentation_framework_json)
    else:
        raise NotImplementedError

    return {'content': argumentation_framework_str,
            'filename': filename + '.' + extension}


@callback(
    Output('24-certain-arguments', 'value'),
    Output('24-certain-attacks', 'value'),
    Output('24-uncertain-arguments', 'value'),
    Output('24-uncertain-attacks', 'value'),
    Input('24-generate-random-af-button', 'n_clicks'),
    Input('24-upload-iaf', 'contents'),
    State('24-upload-iaf', 'filename'),
)
def generate_or_read_iaf(
        _nr_of_clicks_random: int, iaf_content: str, iaf_filename: str):
    """
    Generate a random IAF after clicking the button and put the result in the
    text box.
    """
    if dash.callback_context.triggered_id == '24-generate-random-af-button':
        iaf = IAFGenerator(5, 5, 0.4).generate()
    elif dash.callback_context.triggered_id == '24-upload-iaf':
        content_type, content_str = iaf_content.split(',')
        decoded = base64.b64decode(content_str)

        if iaf_filename.upper().endswith('.JSON'):
            iaf = IAFFromJsonReader().from_json(json.loads(decoded))
        else:
            raise NotImplementedError('This file format is currently not '
                                      'supported.')
    else:
        return '', '', '', ''

    arguments_value = '\n'.join((str(arg)
                                 for arg in iaf.arguments.values()))
    attacks_value = '\n'.join((f'({str(defeat.from_argument)},'
                               f'{str(defeat.to_argument)})'
                               for defeat in iaf.defeats))
    uncertain_arguments_value = '\n'.join((str(arg)
                                           for arg in
                                           iaf.uncertain_arguments.values()))
    uncertain_attacks_value = '\n'.join((f'({str(defeat.from_argument)},'
                                         f'{str(defeat.to_argument)})'
                                         for defeat in iaf.uncertain_defeats))
    return arguments_value, attacks_value, uncertain_arguments_value, \
        uncertain_attacks_value
