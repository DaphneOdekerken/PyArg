import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

from py_arg_learning.identify_grounded_extension import \
    IdentifyGroundedExtension
from py_arg_learning.list_complete_extensions import ListCompleteExtensions
from py_arg_learning.list_preferred_extensions import ListPreferredExtensions

dash.register_page(__name__, name='Learn', title='Learn')

# Get all exercises
exercise_dict = {
    'List all complete extensions': ListCompleteExtensions(),
    'List all preferred extensions': ListPreferredExtensions(),
    'Identify grounded extension': IdentifyGroundedExtension()
}

layout = html.Div(
    children=[
        html.H1('Practice with argumentation exercises'),
        dbc.Col([
            html.B('What would you like to practice?'),
            dbc.Select(options=[{'label': option, 'value': option}
                                for option in exercise_dict.keys()],
                       value=list(exercise_dict.keys())[0],
                       id='exercise-choice-dropdown'),
            html.Br(),
            dbc.Card([], id='explanation-html',
                     className='border-0 bg-transparent'),
            html.Br(),
            dbc.Button('Generate exercise', id='practice-button', n_clicks=0),
            html.Div([
                html.Br(),
                html.Br(),
                dbc.Card([], id='exercise-text',
                         className='border-0 bg-transparent'),
                dbc.Textarea(value='', id='answer-input-text-field',
                             style={'width': '100%'}),
                html.Br(),
                dbc.Button('Check', id='check-button', n_clicks=0),
                html.Br(),
                html.Br(),
                html.Div([], id='feedback-field'),
            ], style={'display': 'none'}, id='30-exercise-div'),
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
          Output('30-exercise-div', 'style'),
          Input('practice-button', 'n_clicks'),
          Input('check-button', 'n_clicks'),
          State('exercise-choice-dropdown', 'value'),
          State('exercise-text', 'children'),
          State('answer-input-text-field', 'value'),
          State('solution-store', 'data'),
          State('30-exercise-div', 'style'),
          State('color-blind-mode', 'on')
          )
def handle_button_click(_generate_button_clicks: int,
                        _check_button_clicks: int,
                        exercise_choice_value: str, old_exercise_text: str,
                        user_solution: str, pre_generated_solutions,
                        old_style: dict, color_blind_mode: bool):
    button_clicked = dash.ctx.triggered_id
    if button_clicked == 'practice-button':
        exercise_set = exercise_dict[exercise_choice_value]
        exercise, graph_data, solutions = \
            exercise_set.generate_exercise_and_solutions(color_blind_mode)
        rendered_exercise = [
            html.B('Exercise'),
            exercise_set.render_exercise_instance(exercise, graph_data)
        ]
        return rendered_exercise, solutions, '', '', {'display': 'block'}
    elif button_clicked == 'check-button':
        exercise_set = exercise_dict[exercise_choice_value]
        feedback_text = exercise_set.get_feedback(user_solution,
                                                  pre_generated_solutions)
        return old_exercise_text, pre_generated_solutions, user_solution, \
            feedback_text, {'display': 'block'}
    return '', [], '', '', old_style
