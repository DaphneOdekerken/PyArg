import base64
import json
import pathlib
from typing import List

import dash
import visdcc
from dash import ctx, html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc

from py_arg.aspic.import_export.argumentation_system_from_json_reader import \
    ArgumentationSystemFromJsonReader
from py_arg.aspic.import_export.argumentation_system_to_json_writer import \
    ArgumentationSystemToJSONWriter
from py_arg.incomplete_aspic.algorithms.relevance.relevance_lister import \
    FourBoolRelevanceLister
from py_arg.incomplete_aspic.algorithms.stability.stability_labeler import \
    StabilityLabeler
from py_arg.incomplete_aspic.classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory
from py_arg_visualisation.functions.graph_data_functions. \
    get_incomplete_aspic_graph_data import get_incomplete_aspic_graph_data

dash.register_page(__name__, name='Inquiry Dialogue System',
                   title='Inquiry Dialogue System')

left_column = dbc.Col(
    [
        html.B('Argumentation system'),
        dbc.Row([
            dbc.Col([dbc.Button('Try fraud example',
                                id='50-fraud-example-button')]),
            dbc.Col([dcc.Upload(dbc.Button('Upload argumentation system'),
                                id='50-chat-as-upload')]),
        ]),
        html.B('Queryables'),
        dcc.Dropdown(multi=True, id='50-queryables-dropdown'),
        html.B('Topic'),
        dcc.Dropdown(id='50-topic-dropdown'),
        html.B('Knowledge base'),
        dcc.Dropdown(id='50-knowledge-base', multi=True, value=[]),
        html.B('Questions'),
        html.Div(id='50-question-input-groups'),
        dcc.Store(id='50-fraud-questions')
    ]
)
right_column = dbc.Col([
    dcc.Tabs([
        dcc.Tab([
            html.B('Topic stability status or next question'),
            html.Div(id='50-stability-status')
        ], label='Frontend'),
        dcc.Tab([
            html.B('Visualisation argumentation theory'),
            visdcc.Network(data={'nodes': [], 'edges': []},
                           id='50-aspic-graph',
                           options={
                               'physics': {'enabled': True},
                               'solver': 'hierarchicalRepulsion',
                               'layout': {'hierarchical':
                                    {'enabled': True,
                                     'direction': 'DU',
                                     'sortMethod': 'directed'}},
                               'wind': {'x': 50, 'y': 50},
                               'improvedLayout': True,
                               'height': '500px',
                               'edges': {'color': {
                                   'inherit': False,
                               }},
                               'interaction': {'hover': True},
                           })
        ], label='Backend')
    ])
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
    Output('50-knowledge-base', 'value'),
    Output('50-fraud-questions', 'data'),
    Input('50-chat-as-upload', 'contents'),
    Input('50-fraud-example-button', 'n_clicks'),
    Input({'type': '50-answer-button', 'queryable_id': ALL}, 'n_clicks'),
    State('50-queryables-dropdown', 'options'),
    State('50-topic-dropdown', 'options'),
    State('50-queryables-dropdown', 'value'),
    State('50-argumentation-system', 'data'),
    State('50-topic-dropdown', 'value'),
    State('50-knowledge-base', 'value'),
    State('50-fraud-questions', 'data'),
    prevent_initial_call=True
)
def update_queryable_and_topic_options(argumentation_system_content,
                                       _fraud_example_clicks,
                                       _answer_button_clicks: List[int],
                                       old_queryables_options,
                                       old_topic_options,
                                       old_queryables_values,
                                       old_argumentation_system,
                                       old_topic_value,
                                       old_knowledge_base: List[str],
                                       old_fraud_questions):
    triggered_id = dash.ctx.triggered_id

    queryable_values = old_queryables_values
    if old_argumentation_system:
        opened_as = ArgumentationSystemFromJsonReader().from_json(
            old_argumentation_system)
    topic_value = old_topic_value
    fraud_questions = old_fraud_questions
    if triggered_id == '50-fraud-example-button':
        # Start trying the fraud example.
        file_path = pathlib.Path(__file__).parent.parent / 'resources' / \
                    '02_2020_COMMA_Paper_Example.json'
        opened_as = ArgumentationSystemFromJsonReader().read_from_json(
            str(file_path))
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
        knowledge = []
        fraud_questions = {
            'citizen_tried_to_buy': 'Did you try to buy a product?',
            'citizen_sent_money': 'Did you send any money?',
            'citizen_sent_product': 'Did you send some product?',
            'citizen_received_product': 'Did you receive some product?',
            'citizen_received_money': 'Did you receive any money?',
            'suspicious_url': 'Was the URL suspect?',
            'screenshot_payment': 'Did the counterparty send you a '
                                  'screenshot to prove payment?',
            'trusted_web_shop': 'Is the web shop on a list of trusted sites?',
        }
    elif triggered_id == '50-chat-as-upload' and argumentation_system_content:
        # Start trying a new example.
        content_type, content_str = argumentation_system_content.split(',')
        decoded = base64.b64decode(content_str)
        opened_as = ArgumentationSystemFromJsonReader().from_json(json.loads(
            decoded))
        queryable_values = []
        topic_value = None
        knowledge = []
        fraud_questions = {}
    elif 'type' in triggered_id and triggered_id['type'] == \
            '50-answer-button':
        # We should add knowledge
        knowledge = old_knowledge_base
        if ctx.triggered[0]['value'] is not None:
            old_knowledge_base.append(triggered_id['queryable_id'])

    else:
        return [], [], [], {}, None, [], {}

    pos_literals = [{'label': key, 'value': key}
                    for key, value in opened_as.language.items()
                    if value.is_positive]
    all_literals = [{'label': key, 'value': key}
                    for key in opened_as.language.keys()]
    as_to_json = ArgumentationSystemToJSONWriter().to_dict(opened_as)
    return pos_literals, all_literals, queryable_values, as_to_json, \
        topic_value, knowledge, fraud_questions


@callback(
    Output('50-knowledge-base', 'options'),
    Output('50-question-input-groups', 'children'),
    Input('50-queryables-dropdown', 'value'),
    Input('50-knowledge-base', 'value'),
    State('50-argumentation-system', 'data'),
    State({'type': '50-question-input', 'queryable_id': ALL}, 'value'),
    State('50-fraud-questions', 'data')
)
def update_knowledge_base_options(queryables, current_value,
                                  argumentation_system_content,
                                  old_questions_by_queryable: List[str],
                                  fraud_questions):
    if not queryables:
        return [], []

    opened_as = ArgumentationSystemFromJsonReader().from_json(
        argumentation_system_content)

    knowledge_base_options = set()
    for queryable_str in queryables:
        queryable_literal = opened_as.language[queryable_str]
        contradictories = \
            [contra for contra in
             queryable_literal.contraries_and_contradictories]
        if not current_value or all(contra.s1 not in current_value
                                    for contra in contradictories):
            knowledge_base_options.add(queryable_str)
            for contradictory in contradictories:
                contra_contradictories = \
                    [contra_contra
                     for contra_contra in
                     contradictory.contraries_and_contradictories]
                if not current_value or \
                        all(contra_contra.s1 not in current_value
                            for contra_contra in contra_contradictories):
                    knowledge_base_options.add(contradictory.s1)
    knowledge_base_options = current_value + list(knowledge_base_options)
    knowledge_base_options_result = \
    [{'label': lit, 'value': lit} for lit in knowledge_base_options]

    old_questions = {}
    for index, question_state in enumerate(ctx.states_list[1]):
        old_questions[question_state['id']['queryable_id']] = \
            old_questions_by_queryable[index]

    query_list_result = []
    for queryable_str in queryables:
        # Check if we should keep some old question
        input_value = ''
        if old_questions and queryable_str in old_questions and \
                old_questions[queryable_str]:
            input_value = old_questions[queryable_str]
        elif fraud_questions and queryable_str in fraud_questions:
            input_value = fraud_questions[queryable_str]

        query_list_result.append(
            dbc.InputGroup([
                dbc.InputGroupText(queryable_str, style={'width': '30%'}),
                dbc.Input(value=input_value,
                          id={'type': '50-question-input',
                              'queryable_id': queryable_str})
            ])
        )

    return knowledge_base_options_result, query_list_result


@callback(
    Output('50-stability-status', 'children'),
    Output('50-aspic-graph', 'data'),
    State('50-queryables-dropdown', 'value'),
    Input('50-knowledge-base', 'value'),
    State('50-argumentation-system', 'data'),
    State('50-topic-dropdown', 'value'),
    Input({'type': '50-question-input', 'queryable_id': ALL}, 'value')
)
def update_stability_status(positive_queryables, knowledge_base,
                            argumentation_system_content, topic_str,
                            question_strs: List[str]):
    if not positive_queryables or not topic_str:
        return [], {}

    opened_as = ArgumentationSystemFromJsonReader().from_json(
        argumentation_system_content)

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

    stability_labeler_labels = StabilityLabeler().label(
        incomplete_argumentation_theory)

    topic_literal = opened_as.language[topic_str]
    topic_label = stability_labeler_labels.literal_labeling[topic_literal]
    if topic_label.is_stable:
        frontend_feedback = html.P('The topic is ' +
                                   topic_label.stability_str.lower() + '.')
        questions = []
    else:
        frontend_feedback = [html.P('The topic is not stable yet.')]
        relevance_lister = FourBoolRelevanceLister()
        relevance_lister.update(incomplete_argumentation_theory,
                                stability_labeler_labels)
        questions = relevance_lister.relevance_list[topic_literal]
        unique_questions = {question.s1.replace('-', '')
                            for question in questions}

        question_dict = {}
        for index, question_state in enumerate(ctx.inputs_list[1]):
            question_dict[question_state['id']['queryable_id']] = \
                question_strs[index]
        for positive_queryable in positive_queryables:
            if positive_queryable not in question_dict or \
                    question_dict[positive_queryable] == '':
                question_dict[positive_queryable] = positive_queryable

        question_list_groups = \
            [dbc.InputGroup([
                dbc.InputGroupText(question_dict[question],
                                   style={'width': '80%'}),
                dbc.ButtonGroup([
                    dbc.Button('Yes',
                               id={'type': '50-answer-button',
                                   'queryable_id': question}),
                    dbc.Button('No',
                               id={'type': '50-answer-button',
                                   'queryable_id': '-' + question})
                ], style={'width': '20%'})
                ])
             for question in unique_questions]

        frontend_feedback += question_list_groups

    graph_data = get_incomplete_aspic_graph_data(
        incomplete_argumentation_theory, stability_labeler_labels,
        topic_literal, questions)

    return frontend_feedback, graph_data
