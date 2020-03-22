from .footer import footer
from .navbar import navbar
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className='mt-4'),
    html.Hr(),
    footer
])