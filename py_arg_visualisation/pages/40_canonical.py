# -*- coding: utf-8 -*-

import dash
import visdcc
from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.algorithms.canonical_constructions import construct_af_adm, construct_af_grd, construct_af_naive, \
    construct_af_stage, construct_af_stb, construct_af_cf, check_tight
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data import get_argumentation_framework_graph_data

dash.register_page(__name__, name='Canonical', title='Canonical')

properties_table = html.Div([html.Table([
    html.Colgroup([
        html.Col(style={}),
        html.Col(id='40-downward-closed-column'),
        html.Col(id='40-tight-column'),
        html.Col(id='40-incomparable-column'),
        html.Col(id='40-dcl-tight-column'),
        html.Col(id='40-conflict-sensitive-column'),
        html.Col(id='40-contains-empty-set-column'),
        html.Col(id='40-one-extension-column'),
        html.Col(style={}),
    ]),
    html.Tr([
        html.Th(),
        html.Th(html.Div(html.Span('Downward-closed')), className='rotate'),
        html.Th(html.Div(html.Span('Tight')), className='rotate'),
        html.Th(html.Div(html.Span('Incomparable')), className='rotate'),
        html.Th(html.Div(html.Span('DCL-tight')), className='rotate'),
        html.Th(html.Div(html.Span('Conflict-sensitive')), className='rotate'),
        html.Th(html.Div(html.Span('Contains empty set')), className='rotate'),
        html.Th(html.Div(html.Span('One extension')), className='rotate'),
        html.Th(),
    ]),
    html.Tr([
        html.Td('Conflict Free'), html.Td('✅'), html.Td('✅'), html.Td('❌'),
        html.Td('❌'), html.Td('❌'), html.Td('❌'),
        html.Td('❌'), html.Td(dbc.Button('Generate', id='40-generate-conflict-free-button'))
    ]),
    html.Tr([
        html.Td('Admissible'), html.Td('✅'), html.Td('✅'), html.Td('❌'),
        html.Td('❌'), html.Td('❌'), html.Td('❌'),
        html.Td('❌'), html.Td(dbc.Button('Generate', id='40-generate-admissible-button'))
    ]),
    html.Tr([
        html.Td('Grounded'), html.Td('✅'), html.Td('✅'), html.Td('❌'),
        html.Td('❌'), html.Td('❌'), html.Td('❌'),
        html.Td('❌'), html.Td(dbc.Button('Generate', id='40-generate-grounded-button'))
    ]),
    html.Tr([
        html.Td('Stable'), html.Td('✅'), html.Td('✅'), html.Td('❌'),
        html.Td('❌'), html.Td('❌'), html.Td('❌'),
        html.Td('❌'), html.Td(dbc.Button('Generate', id='40-generate-stable-button'))
    ]),
    html.Tr([
        html.Td('Naive'), html.Td('✅'), html.Td('✅'), html.Td('❌'),
        html.Td('❌'), html.Td('❌'), html.Td('❌'),
        html.Td('❌'), html.Td(dbc.Button('Generate', id='40-generate-naive-button'))
    ]),
    html.Tr([
        html.Td('Stage'), html.Td('✅'), html.Td('✅'), html.Td('❌'),
        html.Td('❌'), html.Td('❌'), html.Td('❌'),
        html.Td('❌'), html.Td(dbc.Button('Generate', id='40-generate-stage-button'))
    ]),
])])

layout = html.Div(
    children=[
        html.H1('Create canonical AFs based on sets of extensions'),
        dbc.Row([
            dbc.Col([
                html.B('Enter here your set of extensions'),
                dbc.Textarea(id='40-extension-sets-textarea',
                             placeholder='Put each set on a new line and represent sets as {X, Y, Z}.',
                             style={'height': '200px'}),
                html.B('Properties and semantics'),
                properties_table,
            ]),
            dbc.Col(html.Div(id='40-canonical-output-div'))
        ])
    ]
)


def read_extension_sets_from_str(extension_sets_str: str):
    if not extension_sets_str:
        return set()
    extensions_set = extension_sets_str.split('\n')
    input_extension_set = set()
    for extension in extensions_set:
        extension = extension.replace('{', '').replace('}', '')
        argument_strs = [argument_str.strip() for argument_str in extension.split(',')]
        argument_set = frozenset(Argument(argument_str) for argument_str in argument_strs
                                 if argument_str)
        input_extension_set.add(argument_set)
    return input_extension_set


@callback(
    Output('40-downward-closed-column', 'style'),
    Output('40-tight-column', 'style'),
    Output('40-incomparable-column', 'style'),
    Output('40-dcl-tight-column', 'style'),
    Output('40-conflict-sensitive-column', 'style'),
    Output('40-contains-empty-set-column', 'style'),
    Output('40-one-extension-column', 'style'),
    Output('40-generate-conflict-free-button', 'disabled'),
    Output('40-generate-admissible-button', 'disabled'),
    Output('40-generate-grounded-button', 'disabled'),
    Output('40-generate-stable-button', 'disabled'),
    Output('40-generate-naive-button', 'disabled'),
    Output('40-generate-stage-button', 'disabled'),
    Input('40-extension-sets-textarea', 'value')
)
def fill_properties_table(extension_sets_str: str):
    input_extension_set = read_extension_sets_from_str(extension_sets_str)

    # Test which properties hold
    tight = check_tight.apply(input_extension_set)
    if tight:
        tight_style = {'background-color': '#AAAAAA'}
    else:
        tight_style = {}
    # TODO also for other properties

    # TODO: test which semantics can be applied

    return {}, tight_style, {}, {}, {}, {}, {}, \
        False, True, True, True, False, True


@callback(
    Output('40-canonical-output-div', 'children'),
    State('40-extension-sets-textarea', 'value'),
    Input('40-generate-conflict-free-button', 'n_clicks'),
    Input('40-generate-admissible-button', 'n_clicks'),
    Input('40-generate-grounded-button', 'n_clicks'),
    Input('40-generate-stable-button', 'n_clicks'),
    Input('40-generate-naive-button', 'n_clicks'),
    Input('40-generate-stage-button', 'n_clicks'),
    State('color-blind-mode', 'on'),
    prevent_initial_call=True
)
def get_canonical_argumentation_framework(extension_sets_str: str,
                                          _conflict_free_clicks: int,
                                          _admissible_clicks: int,
                                          _grounded_clicks: int,
                                          _stable_clicks: int,
                                          _naive_clicks: int,
                                          _stage_clicks: int,
                                          color_blind_mode: bool):
    input_extension_set = read_extension_sets_from_str(extension_sets_str)

    triggered_id = dash.ctx.triggered_id

    if triggered_id == '40-generate-admissible-button':
        af = construct_af_adm.apply(input_extension_set)
    elif triggered_id == '40-generate-conflict-free-button':
        af = construct_af_cf.apply(input_extension_set)
    elif triggered_id == '40-generate-grounded-button':
        af = construct_af_grd.apply(input_extension_set)
    elif triggered_id == '40-generate-naive-button':
        af = construct_af_naive.apply(input_extension_set)
    elif triggered_id == '40-generate-stage-button':
        af = construct_af_stage.apply(input_extension_set)
    elif triggered_id == '40-generate-stable-button':
        af = construct_af_stb.apply(input_extension_set)
    else:
        raise NotImplementedError

    graph_data = get_argumentation_framework_graph_data(af, None, color_blind_mode)

    return [
        html.B('Canonical argumentation framework'),
        dbc.Col(html.P('AF = (A, D) where A = {{{a}}} and D = {{{d}}}.'.format(
            a=', '.join(str(arg) for arg in af.arguments),
            d='; '.join('(' + str(defeat.from_argument) + ', ' + str(defeat.to_argument) + ')'
                        for defeat in af.defeats)))),
        dbc.Col(visdcc.Network(data=graph_data, options={'height': '500px'}, id='canonical-graph')),
    ]
