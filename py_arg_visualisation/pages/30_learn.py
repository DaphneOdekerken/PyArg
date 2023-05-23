import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

from py_arg_learning.identify_grounded_extension import IdentifyGroundedExtension

dash.register_page(__name__, name='Learn', title='Learn')

# Get all exercises
exercise_dict = {
    'Identify grounded extension': IdentifyGroundedExtension()
}

layout = html.Div(
    children=[
        dbc.Col([
            html.B('What would you like to practice?'),
            dbc.Select(options=[{'label': option, 'value': option} for option in exercise_dict.keys()],
                       value=list(exercise_dict.keys())[0],
                       id='exercise-choice-dropdown'),
            html.Br(),
            dbc.Card([], id='explanation-html'),
            html.Br(),
            dbc.Button('Generate exercise', id='practice-button', n_clicks=0),
            html.Br(),
            html.Br(),
            dbc.Card([], id='exercise-text'),
            dbc.Textarea(value='', id='answer-input-text-field', style={'width': '100%'}),
            html.Br(),
            dbc.Button('Check', id='check-button', n_clicks=0),
            html.Br(),
            html.Br(),
            html.Div([], id='feedback-field'),
            dcc.Store(id='solution-store', data=''),
        ])
    ]
)


@callback(Output('explanation-html', 'children'),
          Input('exercise-choice-dropdown', 'value'))
def get_explanation_html(exercise_choice_value: str):
    exercise_set = exercise_dict[exercise_choice_value]
    return [html.B('Explanation'), exercise_set.get_explanation_html()]


@callback(Output('exercise-text', 'children'),
          Output('solution-store', 'data'),
          Output('answer-input-text-field', 'value'),
          Output('feedback-field', 'children'),
          Input('practice-button', 'n_clicks'),
          Input('check-button', 'n_clicks'),
          State('exercise-choice-dropdown', 'value'),
          State('exercise-text', 'children'),
          State('answer-input-text-field', 'value'),
          State('solution-store', 'data'))
def handle_button_click(_generate_button_clicks: int, _check_button_clicks: int,
                        exercise_choice_value: str, old_exercise_text: str,
                        user_solution: str, pre_generated_solutions):
    button_clicked = dash.ctx.triggered_id
    if button_clicked == 'practice-button':
        exercise_set = exercise_dict[exercise_choice_value]
        exercise, solutions = exercise_set.generate_exercise_and_solutions()
        rendered_exercise = [html.B('Exercise'), exercise_set.render_exercise_instance(exercise)]
        return rendered_exercise, solutions, '', ''
    elif button_clicked == 'check-button':
        exercise_set = exercise_dict[exercise_choice_value]
        feedback_text = exercise_set.get_feedback(user_solution, pre_generated_solutions)
        return old_exercise_text, pre_generated_solutions, user_solution, feedback_text
    return '', [], '', ''
