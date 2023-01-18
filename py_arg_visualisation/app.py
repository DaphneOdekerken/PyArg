from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUMEN])
# server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('PyArg', className='header-title'),
        ], style={'padding': 10, 'flex': 5}),

        html.Div([
            html.Img(src=app.get_asset_url('UU_logo_2021_EN_RGB.png')),
            html.P('Daphne Odekerken and AnneMarie Borg', style={'margin-right': '25px'}),
        ], style={'padding': 10, 'flex': 2, 'text-align': 'right'}),
    ], className='row-container'),

    html.Div(
        [dcc.Link('| ' + page['name'] + ' |', href=page['relative_path'])
         for page in dash.page_registry.values()],
        className='padded-item'
    ),

    html.Div([dash.page_container], className='padded-item')
])
#
# app.layout = html.Div([
#     html.Div([
#         html.Div([
#             html.H1('PyArg', className='header-title'),
#         ], style={'padding': 10, 'flex': 5}),
#
#         html.Div([
#             html.Img(src=app.get_asset_url('UU_logo_2021_EN_RGB.png')),
#             html.P('Daphne Odekerken and AnneMarie Borg', style={'margin-right': '25px'}),
#         ], style={'padding': 10, 'flex': 2, 'text-align': 'right'}),
#     ], className='row-container'),
#
#     html.Div([
#         dcc.RadioItems(
#             id='arg-choice',
#             options=[{'label': 'Abstract', 'value': 'Abstract'}, {'label': 'ASPIC+', 'value': 'ASPIC'}],
#             value='', labelStyle={'display': 'inline-block', 'margin-left': '20px'}),
#     ]),
#     html.Div(id='arg-layout')
# ])

if __name__ == '__main__':
    app.run_server(debug=True)
