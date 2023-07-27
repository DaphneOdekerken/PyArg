from dash import Dash, html
import dash_bootstrap_components as dbc
import dash
import dash_daq as daq


# Create a Dash app using an external stylesheet.
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.YETI])

# Navigation bar.
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Random Abstract AF', href='01-generate-abstract', className='fw-bold'),
                # dbc.DropdownMenuItem('Random ASPIC+ AT', href='02-generate-random-aspic'),
                dbc.DropdownMenuItem('Layered ASPIC+ AS', href='03-generate-layered-aspic', className='fw-bold'),
            ],
            nav=True,
            in_navbar=True,
            label='Generate',
            className='fw-bold',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Abstract', href='21-visualise-abstract', className='fw-bold'),
                dbc.DropdownMenuItem('ASPIC+', href='22-visualise-aspic', className='fw-bold'),
                dbc.DropdownMenuItem('ABA', href='23-visualise-aba', className='fw-bold'),
            ],
            nav=True,
            in_navbar=True,
            label='Visualise', className='fw-bold',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Practice', href='30-learn', className='fw-bold'),
            ],
            nav=True,
            in_navbar=True,
            label='Learn', className='fw-bold',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Canonical Construction AF', href='41-canonical-af', className='fw-bold'),
                dbc.DropdownMenuItem('Canonical Construction ABAF', href='42-canonical-abaf', className='fw-bold')
            ],
            nav=True,
            in_navbar=True,
            label='Algorithms', className='fw-bold',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Chat', href='50-chat', className='fw-bold'),
            ],
            nav=True,
            in_navbar=True,
            label='Applications', className='fw-bold',
        ),
        # dbc.DropdownMenuItem('About', href='/', className='fw-bold'),
        daq.BooleanSwitch(id='color-blind-mode', on=False, className='mt-2'),
        dbc.DropdownMenuItem('Colorblind mode', className='fw-bold text-light')
    ],
    brand='PyArg',
    brand_href='/',
    color='primary', className='fw-bold', dark=True
)

# Specification of the layout, consisting of a navigation bar and the page container.
app.layout = html.Div([navbar, dbc.Col(html.Div([dash.page_container]), width={'size': 10, 'offset': 1})])

# Running the app.
if __name__ == '__main__':
    app.run_server(debug=True)
