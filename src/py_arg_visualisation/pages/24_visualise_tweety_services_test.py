import base64
import json
from typing import List, Dict
import re
import dash
import visdcc
from dash import html, callback, Input, Output, State, ALL, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import ast

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation.generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg.abstract_argumentation.import_export.argumentation_framework_from_aspartix_format_reader import \
    ArgumentationFrameworkFromASPARTIXFormatReader
from py_arg.abstract_argumentation.import_export.argumentation_framework_from_iccma23_format_reader import \
    ArgumentationFrameworkFromICCMA23FormatReader
from py_arg.abstract_argumentation.import_export.argumentation_framework_from_json_reader import \
    ArgumentationFrameworkFromJsonReader
from py_arg.abstract_argumentation.import_export.argumentation_framework_from_trivial_graph_format_reader import \
    ArgumentationFrameworkFromTrivialGraphFormatReader
from py_arg.abstract_argumentation.import_export.argumentation_framework_to_aspartix_format_writer import \
    ArgumentationFrameworkToASPARTIXFormatWriter
from py_arg.abstract_argumentation.import_export.argumentation_framework_to_iccma23_format_writer import \
    ArgumentationFrameworkToICCMA23FormatWriter
from py_arg.abstract_argumentation.import_export.argumentation_framework_to_json_writer import \
    ArgumentationFrameworkToJSONWriter
from py_arg.abstract_argumentation.import_export.argumentation_framework_to_trivial_graph_format_writer import \
    ArgumentationFrameworkToTrivialGraphFormatWriter
from py_arg_visualisation.functions.explanations_functions.explanation_function_options import \
    EXPLANATION_FUNCTION_OPTIONS
from py_arg_visualisation.functions.explanations_functions.get_af_explanations import \
    get_argumentation_framework_explanations
from py_arg_visualisation.functions.extensions_functions.get_accepted_arguments import get_accepted_arguments
from py_arg_visualisation.functions.extensions_functions.get_af_extensions import get_argumentation_framework_extensions
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data
from py_arg_visualisation.functions.import_functions.read_argumentation_framework_functions import \
    read_argumentation_framework

from py_arg_visualisation.functions.tweety_services_functions import tweety_services_handler
from py_arg.abstract_argumentation.classes.argument import Argument
dash.register_page(__name__, name='Visualise Tweety Services Test', title='Visualise Tweety Services')


# Create layout elements and compose them into the layout for this page.

config = tweety_services_handler.TweetyServiceConfig()
config.load()
TWEETY_SERVICES_UP = True

def get_abstract_setting_specification_div():
    return html.Div(children=[
        dcc.Store(id='tweety-selected-argument-store-abstract'),
        dbc.Col([
            dbc.Row([dbc.Col(dbc.Button('Generate random', id='generate-random-af-button', n_clicks=0,
                                        className='w-100')),
                     dbc.Col(dcc.Upload(dbc.Button('Open existing AF', className='w-100'), id='upload-af'))
                     ], className='mt-2'),
            dbc.Row([
                dbc.Col([
                    html.B('Arguments'),
                    dbc.Textarea(id='tweety-arguments',
                                 placeholder='Add one argument per line. For example:\n A\n B\n C',
                                 value='', style={'height': '300px'})
                ]),
                dbc.Col([
                    html.B('Attacks'),
                    dbc.Textarea(id='tweety-attacks',
                                 placeholder='Add one attack per line. For example: \n (A,B) \n (A,C) \n (C,B)',
                                 value='', style={'height': '300px'}),
                ])
            ], className='mt-2'),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText('Filename'),
                    dbc.Input(value='edited_af', id='24-tweety-filename'),
                    dbc.InputGroupText('.'),
                    dbc.Select(options=[{'label': extension, 'value': extension}
                                        for extension in ['JSON', 'TGF', 'APX', 'ICCMA23']],
                               value='JSON', id='24-tweety-extension'),
                    dbc.Button('Download', id='24-tweety-download-button'),
                ], className='mt-2'),
                dcc.Download(id='24-tweety-download')
            ])
        ])
    ])


def get_abstract_evaluation_div():
    try:
        semantics = tweety_services_handler.get_supported_semantics(config)
        semantics_mapping = [{'label': sem, 'value': sem} for sem in semantics]
    except Exception:
        print('Tweety server down')
        TWEETY_SERVICES_UP = False
        semantics_mapping = [             
                    {'label': 'Admissible', 'value': 'Admissible'},
                    {'label': 'Complete', 'value': 'Complete'},
                    {'label': 'Grounded', 'value': 'Grounded'},
                    {'label': 'Preferred', 'value': 'Preferred'},
                    {'label': 'Ideal', 'value': 'Ideal'},
                    {'label': 'Stable', 'value': 'Stable'},
                    {'label': 'Semi-stable', 'value': 'SemiStable'},
                    {'label': 'Eager', 'value': 'Eager'},
                ]

    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.B('Semantics')),
                dbc.Col(dbc.Select(options= semantics_mapping                  
                , value='wad', id='tweety-evaluation-semantics')),
            ]),
            dbc.Row([dbc.Col(html.B('Timeout')),
             dbc.Col(dbc.Input(type='number', min=0, step=1, value=500,
                               id='tweety-timeout-input'))]),
            dbc.Row([
                dbc.Col(html.B('Timeout unit')),
                dbc.Col(dbc.Select(options= [{'label': 'ms', 'value': 'ms'},
                    {'label': 'sec', 'value': 'sec'}]                  
                , value='ms', id='tweety-timeout-unit-input'))]),


            dbc.Row([
                dbc.Col(html.B('Evaluation strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ], value='Credulous', id='tweety-evaluation-strategy')),
            ]),
            dbc.Row(id='tweety-evaluation')
        ]),
    ])


def get_abstract_explanation_div():
    return html.Div([
        dbc.Row([
            dbc.Col(html.B('Type')),
            dbc.Col(dbc.Select(options=[{'label': 'Acceptance', 'value': 'Acceptance'},
                                        {'label': 'Non-Acceptance', 'value': 'NonAcceptance'}],
                               value='Acceptance', id='tweety-explanation-type'))]),
        dbc.Row([
            dbc.Col(html.B('Explanation function')),
            dbc.Col(dbc.Select(id='tweety-explanation-function'))
        ]),
        dbc.Row(id='tweety-explanation')
    ])


left_column = dbc.Col(
    dbc.Accordion([
        dbc.AccordionItem(get_abstract_setting_specification_div(), title='Abstract Argumentation Framework'),
        dbc.AccordionItem(get_abstract_evaluation_div(), title='Evaluation', item_id='Evaluation'),
        dbc.AccordionItem(get_abstract_explanation_div(), title='Explanation', item_id='Explanation')
    ], id='tweety-evaluation-accordion')
)
right_column = dbc.Col([
    dbc.Row([
        dbc.Card(visdcc.Network(data={'nodes': [], 'edges': []}, id='tweety-argumentation-graph',
                                options={'height': '500px'}), body=True),
    ])
])
layout_abstract = dbc.Row([left_column, right_column])
layout = html.Div([html.H1('Visualisation of abstract argumentation frameworks'), layout_abstract])


@callback(
    Output('tweety-arguments', 'value'),
    Output('tweety-attacks', 'value'),
    Input('generate-random-af-button', 'n_clicks'),
    Input('upload-af', 'contents'),
    State('upload-af', 'filename')
)
def generate_abstract_argumentation_framework(_nr_of_clicks_random: int, af_content: str, af_filename: str):
    """
    Generate a random AF after clicking the button and put the result in the text box.
    """
    if dash.callback_context.triggered_id == 'generate-random-af-button':
        random_af = AbstractArgumentationFrameworkGenerator(8, 8, True).generate()
        abstract_arguments_value = '\n'.join((str(arg) for arg in random_af.arguments))
        abstract_attacks_value = '\n'.join((f'({str(defeat.from_argument)},{str(defeat.to_argument)})'
                                            for defeat in random_af.defeats))
        return abstract_arguments_value, abstract_attacks_value
    elif dash.callback_context.triggered_id == 'upload-af':
        content_type, content_str = af_content.split(',')
        decoded = base64.b64decode(content_str)

        name = af_filename.split('.')[0]
        if af_filename.upper().endswith('.JSON'):
            opened_af = ArgumentationFrameworkFromJsonReader().from_json(json.loads(decoded))
        elif af_filename.upper().endswith('.TGF'):
            opened_af = ArgumentationFrameworkFromTrivialGraphFormatReader.from_tgf(decoded.decode(), name)
        elif af_filename.upper().endswith('.APX'):
            opened_af = ArgumentationFrameworkFromASPARTIXFormatReader.from_apx(decoded.decode(), name)
        elif af_filename.upper().endswith('.ICCMA23'):
            opened_af = ArgumentationFrameworkFromICCMA23FormatReader.from_iccma23(decoded.decode(), name)
        else:
            raise NotImplementedError('This file format is currently not supported.')

        abstract_arguments_value = '\n'.join((str(arg) for arg in opened_af.arguments))
        abstract_attacks_value = '\n'.join((f'({str(defeat.from_argument)},{str(defeat.to_argument)})'
                                            for defeat in opened_af.defeats))
        return abstract_arguments_value, abstract_attacks_value
    return '', ''


@callback(
    Output('tweety-argumentation-graph', 'data'),
    Input('tweety-arguments', 'value'),
    Input('tweety-attacks', 'value'),
    Input('tweety-selected-argument-store-abstract', 'data'),
    State('color-blind-mode', 'on'),
    prevent_initial_call=True
)
def create_abstract_argumentation_framework(arguments: str, attacks: str,
                                            selected_arguments: Dict[str, List[str]],
                                            color_blind_mode: bool):
    """
    Send the AF data to the graph for plotting.
    """
    try:
        arg_framework = read_argumentation_framework(arguments, attacks)
    except ValueError:
        arg_framework = AbstractArgumentationFramework()

    if dash.callback_context.triggered_id != 'tweety-selected-argument-store-abstract':
        selected_arguments = None

    data = get_argumentation_framework_graph_data(arg_framework, selected_arguments, color_blind_mode)
    return data


@callback(
    Output('24-tweety-download', 'data'),
    Input('24-tweety-download-button', 'n_clicks'),
    State('tweety-arguments', 'value'),
    State('tweety-attacks', 'value'),
    State('24-tweety-filename', 'value'),
    State('24-tweety-extension', 'value'),
    prevent_initial_call=True,
)
def download_generated_abstract_argumentation_framework(
        _nr_clicks: int, arguments_text: str, defeats_text: str, filename: str, extension: str):
    argumentation_framework = read_argumentation_framework(arguments_text, defeats_text)

    if extension == 'JSON':
        argumentation_framework_json = ArgumentationFrameworkToJSONWriter().to_dict(argumentation_framework)
        argumentation_framework_str = json.dumps(argumentation_framework_json)
    elif extension == 'TGF':
        argumentation_framework_str = \
            ArgumentationFrameworkToTrivialGraphFormatWriter.write_to_str(argumentation_framework)
    elif extension == 'APX':
        argumentation_framework_str = \
            ArgumentationFrameworkToASPARTIXFormatWriter.write_to_str(argumentation_framework)
    elif extension == 'ICCMA23':
        argumentation_framework_str = \
            ArgumentationFrameworkToICCMA23FormatWriter.write_to_str(argumentation_framework)
    else:
        raise NotImplementedError

    return {'content': argumentation_framework_str, 'filename': filename + '.' + extension}


@callback(
    Output('tweety-evaluation', 'children'),
    State('tweety-arguments', 'value'),
    State('tweety-attacks', 'value'),
    Input('tweety-evaluation-accordion', 'active_item'),
    Input('tweety-evaluation-semantics', 'value'),
    Input('tweety-evaluation-strategy', 'value'),
    Input('tweety-timeout-input', 'value'),
    Input('tweety-timeout-unit-input', 'value'),

    prevent_initial_call=True
)
def evaluate_abstract_argumentation_framework(arguments: str, attacks: str,
                                              active_item: str,
                                              semantics: str, strategy: str, timeout:str, unit_timeout = str):
    if active_item != 'Evaluation':
        raise PreventUpdate
    # Read the abstract argumentation framework.
    arg_framework = read_argumentation_framework(arguments, attacks)
    
    time = 0
    status = 'SUCCESS'
    tweety_service_response = ('',-1)

    if TWEETY_SERVICES_UP:
        print(f'{arguments=}')
        print(f'{attacks=}')

        arguments_list = arguments.split('\n')
        nr_arguments = len(arguments_list)
        print(f'{arguments_list=}')
        arguments_id_mapping = dict(zip(arguments_list,range(1,len(arguments_list)+1)))
        # Regular expression pattern to match (A,B) format
        pattern = r'\((\w+),(\w+)\)'

        # Find all matches in the input string
        matches = re.findall(pattern, attacks)
        # Convert matches to actual tuples
        attacks_list = [list(match) for match in matches]
        attacks_id_mapped = [ [arguments_id_mapping[att[0]],arguments_id_mapping[att[1]]] for att in attacks_list]
        config.payload.nr_of_arguments = nr_arguments
        config.payload.attacks = attacks_id_mapped
        config.payload.semantics = semantics
        config.payload.timeout = float(timeout)
        config.payload.unit_timeout = unit_timeout
        tweety_service_response = tweety_services_handler.get_models(config)
        time = tweety_service_response[0]['time']
        unit_time = tweety_service_response[0]['unit_time']
        status = tweety_service_response[0]['status']
        if status == 'SUCCESS':
            try:
                extensions = ast.literal_eval(tweety_service_response[0]['answer'])
                if  not (isinstance(extensions, list) and all(isinstance(item, set) for item in extensions)):
                    # empty extensions get evaluated to dict instead of sets
                    for i,item in enumerate(extensions):
                        if isinstance(item,dict):
                            extensions[i] = set(extensions[i]) 
            except (SyntaxError, ValueError):
                print("Invalid input string.")
        
        # Map ids back to argument names
            id_arguments_mapping = { v:Argument(k) for k,v in arguments_id_mapping.items()} 
            extensions = [set(map(id_arguments_mapping.get, ext)) for ext in extensions]
        
        



    else:

        # Compute the extensions and put them in a list of sets.
        frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
        extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]

        # Make a button for each extension.
    extension_buttons = []
    if status == 'SUCCESS':
        for extension in sorted(extensions):
            out_arguments = {attacked for attacked in arg_framework.arguments
                             if any(argument in arg_framework.get_incoming_defeat_arguments(attacked)
                                    for argument in extension)}
            undecided_arguments = {argument for argument in arg_framework.arguments
                                   if argument not in extension and argument not in out_arguments}
            extension_readable_str = '{' + ', '.join(argument.name for argument in sorted(extension)) + '}'
            extension_in_str = '+'.join(argument.name for argument in sorted(extension))
            extension_out_str = '+'.join(argument.name for argument in sorted(out_arguments))
            extension_undecided_str = '+'.join(argument.name for argument in sorted(undecided_arguments))
            extension_long_str = '|'.join([extension_in_str, extension_undecided_str, extension_out_str])
            extension_buttons.append(dbc.Button([extension_readable_str], color='secondary',
                                                id={'type': 'extension-button-abstract', 'index': extension_long_str}))
        # Based on the extensions, get the acceptance status of arguments.
        accepted_arguments = get_accepted_arguments(extensions, strategy)
        # Mke a button for each accepted argument.
        accepted_argument_buttons = [dbc.Button(argument.name, color='secondary', id={'type': 'argument-button-abstract',
                                                                              'index': argument.name})
                             for argument in sorted(accepted_arguments)]
    else:
        accepted_argument_buttons = []
    return html.Div([html.B('The extension(s):'), html.Div(extension_buttons),
                     html.B('The accepted argument(s):'), html.Div(accepted_argument_buttons),
                     html.P('Click on the extension/argument buttons to display the corresponding argument(s) '
                            'in the graph.'),
                    html.B('Time:'), html.Div(f'{time} {unit_timeout}'),
                    html.B('Status:'), html.Div(status),
                    html.B('Raw Respones:'), html.Div(json.dumps(tweety_service_response[0])),

                    ])


@callback(
    Output('tweety-selected-argument-store-abstract', 'data'),
    Input({'type': 'extension-button-abstract', 'index': ALL}, 'n_clicks'),
    Input({'type': 'argument-button-abstract', 'index': ALL}, 'n_clicks'),
    State('tweety-selected-argument-store-abstract', 'data'),
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
        in_part, undecided_part, out_part = button_clicked_id_index.split('|', 3)
        return {'green': in_part.split('+'), 'yellow': undecided_part.split('+'), 'red': out_part.split('+')}
    elif button_clicked_id_type == 'argument-button-abstract':
        return {'blue': [button_clicked_id_index]}
    return []


@callback(
    Output('tweety-explanation-function', 'options'),
    Output('tweety-explanation-function', 'value'),
    [Input('tweety-explanation-type', 'value')]
)
def setting_choice(choice: str):
    return EXPLANATION_FUNCTION_OPTIONS[choice], EXPLANATION_FUNCTION_OPTIONS[choice][0]['value']


@callback(
    Output('tweety-explanation', 'children'),
    Input('tweety-evaluation-accordion', 'active_item'),
    State('tweety-arguments', 'value'),
    State('tweety-attacks', 'value'),
    State('tweety-evaluation-semantics', 'value'),
    Input('tweety-explanation-function', 'value'),
    Input('tweety-explanation-type', 'value'),
    State('tweety-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def derive_explanations_abstract_argumentation_framework(active_item,
                                                         arguments: str, attacks: str,
                                                         semantics: str, explanation_function: str,
                                                         explanation_type: str, explanation_strategy: str):
    if active_item != 'Explanation':
        raise PreventUpdate

    # Compute the explanations based on the input.
    arg_framework = read_argumentation_framework(arguments, attacks)
    frozen_extensions = get_argumentation_framework_extensions(arg_framework, semantics)
    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
    accepted_arguments = get_accepted_arguments(extensions, explanation_strategy)
    explanations = get_argumentation_framework_explanations(arg_framework, extensions, accepted_arguments,
                                                            explanation_function, explanation_type)
    
    # Print the explanations for each of the arguments.
    return html.Div([html.Div(html.B('Explanation(s) by argument:'))] +
                    [html.Div([
                        html.B(explanation_key),
                        html.Ul([html.Li(str(explanation_value).replace('set()', '{}'))
                                 for explanation_value in explanation_values])])
                     for explanation_key, explanation_values in explanations.items()])
