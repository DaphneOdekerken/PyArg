import dash
import visdcc
from dash import html, callback, Input, Output
import dash_bootstrap_components as dbc

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.algorithms.canonical_constructions import construct_af_adm, construct_af_grd, construct_af_naive, \
    construct_af_stage, construct_af_stb
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data

dash.register_page(__name__, name='Canonical', title='Canonical')

layout = html.Div(
    children=[
        html.H1('Create canonical AFs based on sets of extensions'),
        dbc.Row([
            dbc.Col([
                html.B('Enter here your set of extensions'),
                dbc.Textarea(id='40-extension-sets-textarea',
                             placeholder='Put each set on a new line and represent sets as {X, Y, Z}.',
                             style={'height': '200px'}),
                html.B('Semantics'),
                dbc.Select(options=[
                    {'label': 'Admissible', 'value': 'Admissible'},
                    {'label': 'Grounded', 'value': 'Grounded'},
                    {'label': 'Naive', 'value': 'Naive'},
                    {'label': 'Stage', 'value': 'Stage'},
                    {'label': 'Stable', 'value': 'Stable'},
                ], value='Admissible', id='40-canonical-semantics'),
            ]),
            dbc.Col(html.Div(id='40-canonical-output-div'))
        ])
    ]
)


@callback(
    Output('40-canonical-output-div', 'children'),
    Input('40-extension-sets-textarea', 'value'),
    Input('40-canonical-semantics', 'value'),
    prevent_initial_call=True
)
def get_canonical_argumentation_framework(extension_sets_str: str, semantics: str):

    extensions_set = extension_sets_str.split('\n')
    input_extension_set = set()
    for extension in extensions_set:
        extension = extension.replace('{', '').replace('}', '')
        argument_strs = [argument_str.strip() for argument_str in extension.split(',')]
        argument_set = frozenset(Argument(argument_str) for argument_str in argument_strs
                                 if argument_str)
        input_extension_set.add(argument_set)

    if semantics == 'Admissible':
        af = construct_af_adm.apply(input_extension_set)
    elif semantics == 'Grounded':
        af = construct_af_grd.apply(input_extension_set)
    elif semantics == 'Naive':
        af = construct_af_naive.apply(input_extension_set)
    elif semantics == 'Stage':
        af = construct_af_stage.apply(input_extension_set)
    elif semantics == 'Stable':
        af = construct_af_stb.apply(input_extension_set)
    else:
        # TODO cf?
        raise NotImplementedError

    graph_data = get_argumentation_framework_graph_data(af, None)

    return [
        html.B('Canonical argumentation framework'),
        dbc.Col(html.P('AF = (A, D) where A = {{{a}}} and D = {{{d}}}.'.format(
            a=', '.join(str(arg) for arg in af.arguments),
            d='; '.join('(' + str(defeat.from_argument) + ', ' + str(defeat.to_argument) + ')'
                        for defeat in af.defeats)))),
        dbc.Col(visdcc.Network(data=graph_data, options={'height': '500px'}, id='canonical-graph')),
    ]
