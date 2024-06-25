import pathlib

import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, html, callback, Output, Input, State, dcc

# Create a Dash app using an external stylesheet.
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.YETI])

# Navigation bar.
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Random Abstract AF',
                                     href='01-generate-abstract',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('Random Erdos-Renyi AF',
                                     href='04-generate-erdos-renyi',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('Random Watts-Strogatz AF',
                                     href='05-generate-watts-strogatz',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('Random Barabasi-Albert AF',
                                     href='06-generate-barabasi-albert',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('Layered ASPIC+ AS',
                                     href='03-generate-layered-aspic',
                                     className='fw-bold text-white'),
            ],
            nav=True,
            in_navbar=True,
            label='Generate',
            className='fw-bold',
            toggle_style={'color': 'white'},
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Abstract', href='21-visualise-abstract',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('ASPIC+', href='22-visualise-aspic',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('ABA', href='23-visualise-aba',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('IAF', href='24-visualise-iafs',
                                     className='fw-bold text-white'),
            ],
            nav=True,
            in_navbar=True,
            label='Visualise', className='fw-bold',
            toggle_style={'color': 'white'}
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Practice', href='30-learn',
                                     className='fw-bold text-white'),
            ],
            nav=True,
            in_navbar=True,
            label='Learn', className='fw-bold',
            toggle_style={'color': 'white'}
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Canonical Construction AF',
                                     href='41-canonical-af',
                                     className='fw-bold text-white'),
                dbc.DropdownMenuItem('Canonical Construction ABAF',
                                     href='42-canonical-abaf',
                                     className='fw-bold text-white')
            ],
            nav=True,
            in_navbar=True,
            label='Algorithms', className='fw-bold',
            toggle_style={'color': 'white'},
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Chat', href='50-chat',
                                     className='fw-bold text-white'),
            ],
            nav=True,
            in_navbar=True,
            label='Applications', className='fw-bold',
            toggle_style={'color': 'white'},
        ),
        daq.BooleanSwitch(id='color-blind-mode', on=False, className='mt-2'),
        dbc.DropdownMenuItem('Colorblind mode',
                             className='fw-bold text-white'),
        dbc.Button('📚',
                   id='reference-button', n_clicks=0,
                   outline=True),
        dbc.Tooltip('Click here to obtain background information and '
                    'references for this page.', target='reference-button')
    ],
    brand='PyArg',
    brand_href='/',
    color='primary', className='fw-bold', dark=True
)

reference_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle(
            'Background information and references')),
        dbc.ModalBody(id='reference-modal-body')
    ],
    id='reference-modal',
    size='xl',
    scrollable=True,
    is_open=False
)

# Specification of the layout, consisting of a navigation bar and the page
# container.
app.layout = html.Div([navbar, reference_modal,
                       dcc.Location(id='url-location'),
                       dbc.Col(html.Div([dash.page_container]),
                               width={'size': 10, 'offset': 1})])


@callback(
    Output('reference-modal', 'is_open'),
    Output('reference-modal-body', 'children'),
    Input('reference-button', 'n_clicks'),
    State('reference-modal', 'is_open'),
    State('url-location', 'pathname')
)
def toggle_reference_modal(nr_of_clicks: int, is_open: bool, url_path: str):
    if not nr_of_clicks:
        return is_open, ''

    reference_folder = pathlib.Path.cwd() / 'reference_texts'
    if url_path == '/':
        search_name = '90_pyarg.md'
    else:
        search_name = url_path[1:].replace('-', '_') + '.md'
    search_file = reference_folder / search_name
    if search_file.is_file():
        with open(search_file, 'r') as file:
            latex_explanation = file.read()
    else:
        latex_explanation = \
            f'There was no information for this page ({url_path[1:]}) ' \
            f'available.'

    return not is_open, \
        [html.Div([dcc.Markdown(latex_explanation, mathjax=True,
                                link_target='_blank')])]


# Running the app.
if __name__ == '__main__':
    app.run_server(debug=False)
