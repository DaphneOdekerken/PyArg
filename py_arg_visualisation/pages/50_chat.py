import base64
import json
import pathlib
import random

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

from py_arg.algorithms.relevance.relevance_lister import FourBoolRelevanceLister
from py_arg.algorithms.stability.stability_labeler import StabilityLabeler
from py_arg.import_export.argumentation_system_from_json_reader import ArgumentationSystemFromJsonReader
from py_arg.import_export.argumentation_system_to_json_writer import ArgumentationSystemToJSONWriter
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory

dash.register_page(__name__, name='Inquiry Dialogue System', title='Inquiry Dialogue System')

left_column = dbc.Col(
    [
        html.B('Argumentation system'),
        dbc.Row([
            dbc.Col([dbc.Button('Try fraud example', id='50-fraud-example-button')]),
            dbc.Col([dcc.Upload(dbc.Button('Upload argumentation system'), id='50-chat-as-upload')]),
        ]),
        html.B('Queryables'),
        dcc.Dropdown(multi=True, id='50-queryables-dropdown'),
        html.B('Topic'),
        dcc.Dropdown(id='50-topic-dropdown'),
        html.B('Knowledge base'),
        dcc.Dropdown(id='50-knowledge-base', multi=True, value=[]),
    ]
)
right_column = dbc.Col([
    html.B('Topic stability status or next question'),
    html.P(id='50-stability-status')
])
layout = html.Div([
    html.H1('Argumentation-based inquiry dialogue system'),
    dcc.Store(id='50-argumentation-system'),
    dbc.Row([left_column, right_column])
])


@callback(
    Output('50-queryables-dropdown', 'options'),
    Output('50-topic-dropdown', 'options'),
    Output('50-queryables-dropdown', 'value'),
    Output('50-argumentation-system', 'data'),
    Output('50-topic-dropdown', 'value'),
    Input('50-chat-as-upload', 'contents'),
    Input('50-fraud-example-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_queryable_and_topic_options(argumentation_system_content, _fraud_example_clicks):
    triggered_id = dash.ctx.triggered_id

    if triggered_id == '50-fraud-example-button':
        file_path = pathlib.Path(__file__).parent.parent / 'resources' / '02_2020_COMMA_Paper_Example.json'
        opened_as = ArgumentationSystemFromJsonReader().read_from_json(str(file_path))
        queryable_values = [
            'citizen_tried_to_buy',
            'citizen_sent_money',
            'citizen_sent_product',
            'citizen_received_product',
            'citizen_received_money',
            'suspicious_url',
            'screenshot_payment',
            'trusted_web_shop',
        ]
        topic_value = 'fraud'
    elif triggered_id == '50-chat-as-upload' and argumentation_system_content:
        content_type, content_str = argumentation_system_content.split(',')
        decoded = base64.b64decode(content_str)
        opened_as = ArgumentationSystemFromJsonReader().from_json(json.loads(decoded))
        queryable_values = []
        topic_value = None
    else:
        return [], [], [], {}, None

    pos_literals = [{'label': key, 'value': key}
                    for key, value in opened_as.language.items()
                    if value.is_positive]
    all_literals = [{'label': key, 'value': key} for key in opened_as.language.keys()]
    as_to_json = ArgumentationSystemToJSONWriter().to_dict(opened_as)
    return pos_literals, all_literals, queryable_values, as_to_json, topic_value


@callback(
    Output('50-knowledge-base', 'options'),
    Input('50-queryables-dropdown', 'value'),
    Input('50-knowledge-base', 'value'),
    State('50-argumentation-system', 'data')
)
def update_knowledge_base_options(queryables, current_value, argumentation_system_content):
    if not queryables:
        return []

    opened_as = ArgumentationSystemFromJsonReader().from_json(argumentation_system_content)

    result = set()
    for queryable in queryables:
        queryable_literal = opened_as.language[queryable]
        contradictories = [contra
                           for contra in queryable_literal.contraries_and_contradictories]
        if not current_value or all(contra.s1 not in current_value
                                    for contra in contradictories):
            result.add(queryable)
            for contradictory in contradictories:
                contra_contradictories = \
                    [contra_contra
                     for contra_contra in contradictory.contraries_and_contradictories]
                if not current_value or \
                        all(contra_contra.s1 not in current_value
                            for contra_contra in contra_contradictories):
                    result.add(contradictory.s1)
    result = current_value + list(result)
    return [{'label': lit, 'value': lit} for lit in result]


@callback(
    Output('50-stability-status', 'children'),
    State('50-queryables-dropdown', 'value'),
    Input('50-knowledge-base', 'value'),
    State('50-argumentation-system', 'data'),
    State('50-topic-dropdown', 'value')
)
def update_knowledge_base_options(positive_queryables, knowledge_base,
                                  argumentation_system_content, topic_str):
    if not positive_queryables or not topic_str:
        return ''

    opened_as = ArgumentationSystemFromJsonReader().from_json(argumentation_system_content)

    queryables = set()
    for q in positive_queryables:
        positive_queryable = opened_as.language[q]
        queryables.add(positive_queryable)
        for q_contra in positive_queryable.contraries_and_contradictories:
            queryables.add(q_contra)

    incomplete_argumentation_theory = IncompleteArgumentationTheory(
        argumentation_system=opened_as,
        queryables=list(queryables),
        knowledge_base_axioms=[opened_as.language[k] for k in knowledge_base],
        knowledge_base_ordinary_premises=[]
    )

    stability_labeler_labels = StabilityLabeler().label(incomplete_argumentation_theory)
    topic_literal = opened_as.language[topic_str]
    topic_label = stability_labeler_labels.literal_labeling[topic_literal]
    if topic_label.is_stable:
        return 'The topic is ' + topic_label.stability_str.lower() + '.'

    relevance_lister = FourBoolRelevanceLister()
    relevance_lister.update(incomplete_argumentation_theory, stability_labeler_labels)
    questions = relevance_lister.relevance_list[topic_literal]
    random_question = random.choice(list(questions))
    return 'The topic is not stable yet. Do you know something about ' + random_question.s1 + '?'
