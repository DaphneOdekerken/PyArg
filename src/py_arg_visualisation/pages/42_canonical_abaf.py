# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import visdcc
from dash import html, callback, Input, Output, State

from py_arg.abstract_argumentation.canonical_constructions import \
    check_intersection_in, check_set_com_closed
from py_arg.abstract_argumentation.canonical_constructions import \
    check_set_conf_sens
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_non_empty, is_downward_closed, \
    contains_empty_set
from py_arg.assumption_based_argumentation.canonical_constructions import \
    construct_abaf_com, construct_abaf_prf, \
    construct_abaf_st, construct_abaf_cf, construct_abaf_naive, \
    construct_abaf_adm
from py_arg_visualisation.functions.graph_data_functions.get_af_graph_data \
    import get_argumentation_framework_graph_data

dash.register_page(__name__, name='CanonicalABAF', title='CanonicalABAF')

properties_table = html.Div([html.Table([
    html.Colgroup([
        html.Col(style={}),
        html.Col(id='42-incomparable-column'),
        html.Col(id='42-nonempty-column'),
        html.Col(id='42-downward-closed-column'),
        html.Col(id='42-set-conflict-sensitive-column'),
        html.Col(id='42-contains-empty-set-column'),
        html.Col(id='42-set-comp-closed-column'),
        html.Col(id='42-contains-intersection-column'),
        html.Col(style={}),
    ]),
    html.Tr([
        html.Th(),
        html.Th(html.Div(html.Span('Incomparable')), className='rotate'),
        html.Th(html.Div(html.Span('Non-Empty')), className='rotate'),
        html.Th(html.Div(html.Span('Downward-closed')), className='rotate'),
        html.Th(html.Div(html.Span('Set-Conflict-Sensitive')),
                className='rotate'),
        html.Th(html.Div(html.Span('Contains Empty Set')), className='rotate'),
        html.Th(html.Div(html.Span('Set-Comp-Closed')), className='rotate'),
        html.Th(html.Div(html.Span('Contains-Intersection')),
                className='rotate'),
        html.Th(),
    ]),
    html.Tr([
        html.Td('Stable'),
        html.Td(id='42-stb-incomparable'),
        html.Td(), html.Td(), html.Td(), html.Td(), html.Td(), html.Td(),
        html.Td(dbc.Button('Generate', id='42-generate-stable-button'))
    ]),
    html.Tr([
        html.Td('Preferred'),
        html.Td(id='42-pref-incomparable'),
        html.Td(id='42-pref-non-empty'),
        html.Td(), html.Td(), html.Td(), html.Td(), html.Td(),
        html.Td(dbc.Button('Generate', id='42-generate-preferred-button'))
    ]),
    html.Tr([
        html.Td('Conflict-Free'),
        html.Td(),
        html.Td(id='42-cf-non-empty'),
        html.Td(id='42-cf-downward-closed'),
        html.Td(), html.Td(), html.Td(), html.Td(),
        html.Td(dbc.Button('Generate', id='42-generate-cf-button'))
    ]),
    html.Tr([
        html.Td('Naive'),
        html.Td(id='42-naive-incomparable'),
        html.Td(id='42-naive-non-empty'),
        html.Td(), html.Td(), html.Td(), html.Td(), html.Td(),
        html.Td(dbc.Button('Generate', id='42-generate-naive-button'))
    ]),
    html.Tr([
        html.Td('Admissible'),
        html.Td(),
        html.Td(id='42-adm-non-empty'),
        html.Td(),
        html.Td(id='42-adm-set-conf-sensitive'),
        html.Td(id='42-adm-contains-empty'),
        html.Td(),
        html.Td(),
        html.Td(dbc.Button('Generate', id='42-generate-adm-button'))
    ]),
    html.Tr([
        html.Td('Complete'),
        html.Td(),
        html.Td(id='42-com-non-empty'),
        html.Td(),
        html.Td(),
        html.Td(),
        html.Td(id='42-com-set-comp-closed'),
        html.Td(id='42-com-contains-intersection'),
        html.Td(dbc.Button('Generate', id='42-generate-complete-button'))
    ]),
])])

layout = html.Div(
    children=[
        html.H1('Create canonical ABAFs based on sets of extensions'),
        dbc.Row([
            dbc.Col([
                html.B('Enter your set of extensions here'),
                dbc.Textarea(id='42-extension-sets-textarea',
                             placeholder='Put each set on a new line and '
                                         'represent sets as {X, Y, Z}.',
                             style={'height': '200px'}),
                html.B('Properties and semantics'),
                properties_table,
            ]),
            dbc.Col(html.Div(id='42-canonical-output-div'))
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
        argument_set = frozenset(argument_str for argument_str in argument_strs
                                 if argument_str)
        input_extension_set.add(argument_set)
    return input_extension_set


@callback(
    Output('42-incomparable-column', 'style'),
    Output('42-nonempty-column', 'style'),
    Output('42-downward-closed-column', 'style'),
    Output('42-set-conflict-sensitive-column', 'style'),
    Output('42-contains-empty-set-column', 'style'),
    Output('42-set-comp-closed-column', 'style'),
    Output('42-contains-intersection-column', 'style'),
    Output('42-generate-stable-button', 'disabled'),
    Output('42-generate-preferred-button', 'disabled'),
    Output('42-generate-cf-button', 'disabled'),
    Output('42-generate-naive-button', 'disabled'),
    Output('42-generate-adm-button', 'disabled'),
    Output('42-generate-complete-button', 'disabled'),
    Output('42-stb-incomparable', 'children'),
    Output('42-pref-incomparable', 'children'),
    Output('42-pref-non-empty', 'children'),
    Output('42-cf-non-empty', 'children'),
    Output('42-cf-downward-closed', 'children'),
    Output('42-naive-incomparable', 'children'),
    Output('42-naive-non-empty', 'children'),
    Output('42-adm-non-empty', 'children'),
    Output('42-adm-set-conf-sensitive', 'children'),
    Output('42-adm-contains-empty', 'children'),
    Output('42-com-non-empty', 'children'),
    Output('42-com-set-comp-closed', 'children'),
    Output('42-com-contains-intersection', 'children'),
    Input('42-extension-sets-textarea', 'value')
)
def fill_properties_table(extension_sets_str: str):
    input_extension_set = read_extension_sets_from_str(extension_sets_str)

    green = '#CCFFCC'
    red = '#FFCCCC'

    positive_icon = '✅'
    negative_icon = '❌'

    # Test which properties hold
    incomparable = is_incomparable(input_extension_set)
    if incomparable:
        incomparable_style = {'background-color': green}
        incomparable_value = positive_icon
    else:
        incomparable_style = {'background-color': red}
        incomparable_value = negative_icon
    non_empty = is_non_empty(input_extension_set)
    if non_empty:
        non_empty_style = {'background-color': green}
        non_empty_value = positive_icon
    else:
        non_empty_style = {'background-color': red}
        non_empty_value = negative_icon
    downward_closed = is_downward_closed(input_extension_set)
    if downward_closed:
        downward_closed_style = {'background-color': green}
        downward_closed_value = positive_icon
    else:
        downward_closed_style = {'background-color': red}
        downward_closed_value = negative_icon
    set_conf_sens = check_set_conf_sens.apply(input_extension_set)
    if incomparable:
        set_conf_sens_style = {'background-color': green}
        set_conf_sens_value = positive_icon
    else:
        set_conf_sens_style = {'background-color': red}
        set_conf_sens_value = negative_icon
    contains_empty = contains_empty_set(input_extension_set)
    if contains_empty:
        contains_empty_style = {'background-color': green}
        contains_empty_value = positive_icon
    else:
        contains_empty_style = {'background-color': red}
        contains_empty_value = negative_icon
    set_comp_closed = check_set_com_closed.apply(input_extension_set)
    if set_comp_closed:
        set_comp_closed_style = {'background-color': green}
        set_comp_closed_value = positive_icon
    else:
        set_comp_closed_style = {'background-color': red}
        set_comp_closed_value = negative_icon
    intersection_in = check_intersection_in.apply(input_extension_set)
    if intersection_in:
        intersection_in_style = {'background-color': green}
        intersection_in_value = positive_icon
    else:
        intersection_in_style = {'background-color': red}
        intersection_in_value = negative_icon

    stb_realizable = incomparable
    pref_realizable = incomparable and non_empty
    cf_realizable = non_empty and downward_closed
    naive_realizable = incomparable and non_empty
    adm_realizable = non_empty and set_conf_sens and contains_empty
    com_realizable = non_empty and set_comp_closed and intersection_in

    return incomparable_style, non_empty_style, downward_closed_style, \
        set_conf_sens_style, contains_empty_style, \
        set_comp_closed_style, intersection_in_style, \
        not stb_realizable, not pref_realizable, not cf_realizable, \
        not naive_realizable, not adm_realizable, \
        not com_realizable, \
        incomparable_value, \
        incomparable_value, non_empty_value, \
        non_empty_value, downward_closed_value, \
        incomparable_value, non_empty_value, \
        non_empty_value, set_conf_sens_value, contains_empty_value, \
        non_empty_value, set_comp_closed_value, intersection_in_value


@callback(
    Output('42-canonical-output-div', 'children'),
    State('42-extension-sets-textarea', 'value'),
    Input('42-generate-stable-button', 'n_clicks'),
    Input('42-generate-preferred-button', 'n_clicks'),
    Input('42-generate-cf-button', 'n_clicks'),
    Input('42-generate-naive-button', 'n_clicks'),
    Input('42-generate-adm-button', 'n_clicks'),
    Input('42-generate-complete-button', 'n_clicks'),
    State('color-blind-mode', 'on'),
    prevent_initial_call=True
)
def get_canonical_argumentation_framework(extension_sets_str: str,
                                          _stb_clicks: int,
                                          _pref_clicks: int,
                                          _cf_clicks: int,
                                          _naive_clicks: int,
                                          _adm_clicks: int,
                                          _com_clicks: int,
                                          color_blind_mode: bool):
    input_extension_set = read_extension_sets_from_str(extension_sets_str)

    triggered_id = dash.ctx.triggered_id

    if triggered_id == '42-generate-stable-button':
        abaf = construct_abaf_st.apply(input_extension_set)
    elif triggered_id == '42-generate-preferred-button':
        abaf = construct_abaf_prf.apply(input_extension_set)
    elif triggered_id == '42-generate-cf-button':
        abaf = construct_abaf_cf.apply(input_extension_set)
    elif triggered_id == '42-generate-naive-button':
        abaf = construct_abaf_naive.apply(input_extension_set)
    elif triggered_id == '42-generate-adm-button':
        abaf = construct_abaf_adm.apply(input_extension_set)
    elif triggered_id == '42-generate-complete-button':
        abaf = construct_abaf_com.apply(input_extension_set)
    else:
        raise NotImplementedError

    graph_data = get_argumentation_framework_graph_data(abaf.generate_af(),
                                                        None, color_blind_mode)

    return [
        html.B('Canonical ABA framework'),
        dbc.Col(html.P(
            'D = (L, R, A, C) where L = {{{l}}}, R = {{{r}}}, '
            'A = {{{a}}} and C = {{{c}}}.'.format(
                l=', '.join(str(atom) for atom in abaf.language),
                r='; '.join(str(rule) for rule in abaf.rules),
                a=', '.join(str(atom) for atom in abaf.assumptions),
                c='; '.join('(' + str(atom) + ', ' +
                            str(abaf.contraries[atom]) + ')'
                            for atom in abaf.contraries.keys())))),
        dbc.Col(visdcc.Network(data=graph_data, options={'height': '500px'},
                               id='canonical-graph')),
    ]
