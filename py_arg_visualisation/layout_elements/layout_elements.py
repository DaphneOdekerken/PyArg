from dash import html, dcc

from py_arg_visualisation.layout_elements.abstract_argumentation_layout_elements import get_abstract_layout, \
    get_abstract_explanation, get_abstract_evaluation, get_abstract_setting
from py_arg_visualisation.layout_elements.structured_argumentation_layout_elements import get_aspic_layout, \
    get_structured_explanation, get_structured_evaluation, get_aspic_setting


def get_layout_elements(app):
    abstract_setting = get_abstract_setting()
    ASPIC_setting = get_aspic_setting()
    abstract_evaluation = get_abstract_evaluation()
    structured_evaluation = get_structured_evaluation()
    abstract_explanation = get_abstract_explanation()
    structured_explanation = get_structured_explanation()
    layout_abstract = get_abstract_layout(abstract_evaluation, abstract_explanation, abstract_setting)
    layout_ASPIC = get_aspic_layout(ASPIC_setting, structured_evaluation, structured_explanation)
    app_layout = get_app_layout(app)
    app_validation_layout = get_app_validation_layout(ASPIC_setting, abstract_evaluation, abstract_explanation,
                                                      abstract_setting, structured_evaluation)
    return app_layout, app_validation_layout, layout_abstract, layout_ASPIC


def get_app_validation_layout(ASPIC_setting, abstract_evaluation, abstract_explanation, abstract_setting,
                              structured_evaluation):
    app_validation_layout = html.Div([
        abstract_setting,
        ASPIC_setting,
        abstract_evaluation,
        structured_evaluation,
        abstract_explanation
    ])
    return app_validation_layout


def get_app_layout(app):
    app_layout = html.Div([
        html.Div([
            html.Div([
                html.H1('PyArg', className='header-title'),
            ], style={'padding': 10, 'flex': 5}),

            html.Div([
                html.Img(src=app.get_asset_url('UU_logo_2021_EN_RGB.png'),
                         style={'border': 'none', 'width': '30%', 'max-width': '500px', 'align': 'right',
                                'margin-right': '20px'}),
                html.P('Daphne Odekerken and AnneMarie Borg', style={'margin-right': '25px'}),
            ], style={'padding': 10, 'flex': 2, 'text-align': 'right'}),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div([
            dcc.RadioItems(
                id='arg-choice',
                options=[
                    {'label': 'Abstract', 'value': 'Abstract'},
                    {'label': 'ASPIC+', 'value': 'ASPIC'}
                ],
                value='',
                labelStyle={'display': 'inline-block', 'margin-left': '20px'},
                inputStyle={'margin-right': '6px'}),
        ]),
        html.Div(id='arg-layout')
    ])
    return app_layout
