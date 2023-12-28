# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import visdcc
from dash import html, callback, Input, Output, State

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    construct_af_cf import \
    construct_argumentation_framework_conflict_free
from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    construct_af_grd import construct_argumentation_framework_grounded
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_conflict_sensitive, is_incomparable, is_tight, is_dcl_tight, \
    is_non_empty, is_downward_closed, is_unary, contains_empty_set
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .construct_af_stage import construct_argumentation_framework_stage
from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    construct_af_adm import construct_argumentation_framework_admissible
from py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .construct_af_naive import construct_argumentation_framework_naive
from py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .construct_af_stb import construct_argumentation_framework_stable
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data \
    import get_argumentation_framework_graph_data

dash.register_page(__name__, name='Canonical', title='Canonical')

properties_table = html.Div([html.Table([
    html.Colgroup([
        html.Col(style={}),
        html.Col(id='41-tight-column'),
        html.Col(id='41-conflict-sensitive-column'),
        html.Col(id='41-downward-closed-column'),
        html.Col(id='41-incomparable-column'),
        html.Col(id='41-dcl-tight-column'),
        html.Col(id='41-contains-empty-set-column'),
        html.Col(id='41-nonempty-column'),
        html.Col(id='41-unary-column'),
        html.Col(style={}),
    ]),
    html.Tr([
        html.Th(),
        html.Th(html.Div(html.Span('Tight')), className='rotate'),
        html.Th(html.Div(html.Span('Conflict-sensitive')), className='rotate'),
        html.Th(html.Div(html.Span('Downward-closed')), className='rotate'),
        html.Th(html.Div(html.Span('Incomparable')), className='rotate'),
        html.Th(html.Div(html.Span('DCL-tight')), className='rotate'),
        html.Th(html.Div(html.Span('Contains empty set')), className='rotate'),
        html.Th(html.Div(html.Span('Nonempty')), className='rotate'),
        html.Th(html.Div(html.Span('Unary')), className='rotate'),
        html.Th(),
    ]),
    html.Tr([
        html.Td('Conflict Free'),
        html.Td(id='41-cf-tight'), html.Td(),
        html.Td(id='41-cf-downward-closed'),
        html.Td(), html.Td(), html.Td(),
        html.Td(id='41-cf-non-empty'),
        html.Td(), html.Td(dbc.Button('Generate',
                                      id='41-generate-conflict-free-button'))
    ]),
    html.Tr([
        html.Td('Admissible'), html.Td(),
        html.Td(id='41-adm-conflict-sensitive'), html.Td(),
        html.Td(), html.Td(),
        html.Td(id='41-adm-contains-empty'),
        html.Td(id='41-adm-non-empty'),
        html.Td(), html.Td(dbc.Button('Generate',
                                      id='41-generate-admissible-button'))
    ]),
    html.Tr([
        html.Td('Grounded'), html.Td(), html.Td(), html.Td(),
        html.Td(), html.Td(), html.Td(), html.Td(),
        html.Td(id='41-gr-unary'),
        html.Td(dbc.Button('Generate', id='41-generate-grounded-button'))
    ]),
    html.Tr([
        html.Td('Stable'), html.Td(id='41-stb-tight'),
        html.Td(), html.Td(), html.Td(id='41-stb-incomparable'),
        html.Td(),
        html.Td(), html.Td(),
        html.Td(), html.Td(dbc.Button('Generate',
                                      id='41-generate-stable-button'))
    ]),
    html.Tr([
        html.Td('Naive'), html.Td(), html.Td(), html.Td(),
        html.Td(id='41-na-incomparable'),
        html.Td(id='41-na-dcl-tight'), html.Td(),
        html.Td(id='41-na-non-empty'),
        html.Td(), html.Td(dbc.Button('Generate',
                                      id='41-generate-naive-button'))
    ]),
    html.Tr([
        html.Td('Stage'), html.Td(id='41-stg-tight'),
        html.Td(), html.Td(),
        html.Td(id='41-stg-incomparable'),
        html.Td(), html.Td(),
        html.Td(id='41-stg-non-empty'),
        html.Td(), html.Td(dbc.Button('Generate',
                                      id='41-generate-stage-button'))
    ]),
])])

layout = html.Div(
    children=[
        html.H1('Create canonical AFs based on sets of extensions'),
        dbc.Row([
            dbc.Col([
                html.B('Enter your set of extensions here'),
                dbc.Textarea(id='41-extension-sets-textarea',
                             placeholder='Put each set on a new line and '
                                         'represent sets as {X, Y, Z}.',
                             style={'height': '200px'}),
                html.B('Properties and semantics'),
                properties_table,
            ]),
            dbc.Col(html.Div(id='41-canonical-output-div'))
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
        argument_strs = [argument_str.strip()
                         for argument_str in extension.split(',')]
        argument_set = frozenset(Argument(argument_str)
                                 for argument_str in argument_strs
                                 if argument_str)
        input_extension_set.add(argument_set)
    return input_extension_set


@callback(
    Output('41-tight-column', 'style'),
    Output('41-conflict-sensitive-column', 'style'),
    Output('41-downward-closed-column', 'style'),
    Output('41-incomparable-column', 'style'),
    Output('41-dcl-tight-column', 'style'),
    Output('41-contains-empty-set-column', 'style'),
    Output('41-nonempty-column', 'style'),
    Output('41-unary-column', 'style'),
    Output('41-generate-conflict-free-button', 'disabled'),
    Output('41-generate-admissible-button', 'disabled'),
    Output('41-generate-grounded-button', 'disabled'),
    Output('41-generate-stable-button', 'disabled'),
    Output('41-generate-naive-button', 'disabled'),
    Output('41-generate-stage-button', 'disabled'),
    Output('41-cf-tight', 'children'),
    Output('41-cf-downward-closed', 'children'),
    Output('41-cf-non-empty', 'children'),
    Output('41-adm-conflict-sensitive', 'children'),
    Output('41-adm-contains-empty', 'children'),
    Output('41-adm-non-empty', 'children'),
    Output('41-gr-unary', 'children'),
    Output('41-stb-tight', 'children'),
    Output('41-stb-incomparable', 'children'),
    Output('41-na-incomparable', 'children'),
    Output('41-na-dcl-tight', 'children'),
    Output('41-na-non-empty', 'children'),
    Output('41-stg-tight', 'children'),
    Output('41-stg-incomparable', 'children'),
    Output('41-stg-non-empty', 'children'),
    Input('41-extension-sets-textarea', 'value')
)
def fill_properties_table(extension_sets_str: str):
    input_extension_set = read_extension_sets_from_str(extension_sets_str)

    green = '#CCFFCC'
    red = '#FFCCCC'

    positive_icon = '✅'
    negative_icon = '❌'

    # Test which properties hold
    tight = is_tight(input_extension_set)
    if tight:
        tight_style = {'background-color': green}
        tight_value = positive_icon
    else:
        tight_style = {'background-color': red}
        tight_value = negative_icon
    conf_sens = is_conflict_sensitive(input_extension_set)
    if conf_sens:
        conf_sens_style = {'background-color': green}
        conf_sens_value = positive_icon
    else:
        conf_sens_style = {'background-color': red}
        conf_sens_value = negative_icon
    downward_closed = is_downward_closed(input_extension_set)
    if downward_closed:
        downward_closed_style = {'background-color': green}
        downward_closed_value = positive_icon
    else:
        downward_closed_style = {'background-color': red}
        downward_closed_value = negative_icon
    incomparable = is_incomparable(input_extension_set)
    if incomparable:
        incomparable_style = {'background-color': green}
        incomparable_value = positive_icon
    else:
        incomparable_style = {'background-color': red}
        incomparable_value = negative_icon
    dcl_tight = is_dcl_tight(input_extension_set)
    if dcl_tight:
        dcl_tight_style = {'background-color': green}
        dcl_tight_value = positive_icon
    else:
        dcl_tight_style = {'background-color': red}
        dcl_tight_value = negative_icon
    contains_empty = contains_empty_set(input_extension_set)
    if contains_empty:
        contains_empty_style = {'background-color': green}
        contains_empty_value = positive_icon
    else:
        contains_empty_style = {'background-color': red}
        contains_empty_value = negative_icon
    unary = is_unary(input_extension_set)
    if unary:
        unary_style = {'background-color': green}
        unary_value = positive_icon
    else:
        unary_style = {'background-color': red}
        unary_value = negative_icon
    non_empty = is_non_empty(input_extension_set)
    if non_empty:
        non_empty_style = {'background-color': green}
        non_empty_value = positive_icon
    else:
        non_empty_style = {'background-color': red}
        non_empty_value = negative_icon

    cf_realizable = downward_closed and tight and non_empty
    adm_realizable = contains_empty and non_empty and conf_sens
    grd_realizable = unary
    stb_realizable = tight and incomparable
    naive_realizable = non_empty and incomparable and dcl_tight
    stg_realizable = tight and incomparable and non_empty

    return tight_style, conf_sens_style, downward_closed_style, \
        incomparable_style, dcl_tight_style, \
        contains_empty_style, non_empty_style, unary_style, \
        not cf_realizable, not adm_realizable, not grd_realizable, \
        not stb_realizable, not naive_realizable, \
        not stg_realizable, \
        tight_value, downward_closed_value, non_empty_value, \
        conf_sens_value, contains_empty_value, non_empty_value, \
        unary_value, \
        tight_value, incomparable_value, \
        incomparable_value, dcl_tight_value, non_empty_value, \
        tight_value, incomparable_value, non_empty_value


@callback(
    Output('41-canonical-output-div', 'children'),
    State('41-extension-sets-textarea', 'value'),
    Input('41-generate-conflict-free-button', 'n_clicks'),
    Input('41-generate-admissible-button', 'n_clicks'),
    Input('41-generate-grounded-button', 'n_clicks'),
    Input('41-generate-stable-button', 'n_clicks'),
    Input('41-generate-naive-button', 'n_clicks'),
    Input('41-generate-stage-button', 'n_clicks'),
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

    if triggered_id == '41-generate-admissible-button':
        af = construct_argumentation_framework_admissible(input_extension_set)
    elif triggered_id == '41-generate-conflict-free-button':
        af = construct_argumentation_framework_conflict_free(
            input_extension_set)
    elif triggered_id == '41-generate-grounded-button':
        af = construct_argumentation_framework_grounded(input_extension_set)
    elif triggered_id == '41-generate-naive-button':
        af = construct_argumentation_framework_naive(input_extension_set)
    elif triggered_id == '41-generate-stage-button':
        af = construct_argumentation_framework_stage(input_extension_set)
    elif triggered_id == '41-generate-stable-button':
        af = construct_argumentation_framework_stable(input_extension_set)
    else:
        raise NotImplementedError

    graph_data = get_argumentation_framework_graph_data(
        af, None, color_blind_mode)

    return [
        html.B('Canonical argumentation framework'),
        dbc.Col(html.P('AF = (A, D) where A = {{{a}}} and D = {{{d}}}.'.format(
            a=', '.join(str(arg) for arg in af.arguments),
            d='; '.join('(' + str(defeat.from_argument) + ', ' + str(
                defeat.to_argument) + ')'
                        for defeat in af.defeats)))),
        dbc.Col(visdcc.Network(data=graph_data, options={'height': '500px'},
                               id='canonical-graph')),
    ]
