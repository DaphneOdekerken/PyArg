import dash
from dash import html, dcc, callback, Input, Output, State

from py_arg_learning.identify_grounded_extension import IdentifyGroundedExtension

dash.register_page(__name__)

# Get all exercises
exercise_dict = {
    'Identify grounded extension': IdentifyGroundedExtension()
}

layout = html.Div(
    children=[
        html.H1('This is the argumentation learning home page.'),
        html.Div([
            html.P('What would you like to practice?'),
            dcc.Dropdown(options=list(exercise_dict.keys()), value=list(exercise_dict.keys())[0],
                         id='exercise-choice-dropdown'),
            html.Br(),
            html.Div([], id='explanation-html'),
            html.Br(),
            html.Button('Generate exercise', id='practice-button', n_clicks=0, className='small-pyarg-button'),
            html.Br(),
            html.Br(),
            html.Div([], id='exercise-text'),
            dcc.Textarea(value='', id='answer-input-text-field', style={'width': '100%'}),
            html.Br(),
            html.Button('Check', id='check-button', n_clicks=0, className='small-pyarg-button'),
            html.Br(),
            html.Br(),
            html.Div([], id='feedback-field'),
            dcc.Store(id='solution-store', data=''),
        ], style={'width': '800px'})
    ]
)


@callback(Output('explanation-html', 'children'),
          Input('exercise-choice-dropdown', 'value'))
def get_explanation_html(exercise_choice_value: str):
    exercise_set = exercise_dict[exercise_choice_value]
    return exercise_set.get_explanation_html()


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
def handle_button_click(generate_button_clicks: int, check_button_clicks: int,
                        exercise_choice_value: str, old_exercise_text: str,
                        user_solution: str, pre_generated_solutions):
    button_clicked = dash.ctx.triggered_id
    if button_clicked == 'practice-button':
        exercise_set = exercise_dict[exercise_choice_value]
        exercise, solutions = exercise_set.generate_exercise_and_solutions()
        rendered_exercise = exercise_set.render_exercise_instance(exercise)
        return rendered_exercise, solutions, '', ''
    elif button_clicked == 'check-button':
        exercise_set = exercise_dict[exercise_choice_value]
        feedback_text = exercise_set.get_feedback(user_solution, pre_generated_solutions)
        return old_exercise_text, pre_generated_solutions, user_solution, feedback_text
    return '', [], '', ''
