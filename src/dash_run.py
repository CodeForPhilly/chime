import os

import dash_core_components as dcc
from dash.dependencies import Input, Output

from penn_chime_dash.app import init_app
from penn_chime_dash.app.components.layout import layout
from penn_chime_dash.app.pages import about, chime, contact, contribute, index

PENN_CHIME = init_app('dev')
PENN_CHIME.layout = layout
server = PENN_CHIME.server
PENN_CHIME.title = "Penn-CHIME"

@PENN_CHIME.callback(Output('page-content', 'children'),
                    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/CHIME':
        return chime.layout
    elif pathname == '/contact':
        return contact.layout
    elif pathname == '/contribute':
        return contribute.layout
    elif pathname == '/about':
        return about.layout
    else:
        return dcc.Markdown('## Page not found')

if __name__ == '__main__':
    PENN_CHIME.run_server(debug=True)
