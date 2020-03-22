import os
from app import init_app
import dash_core_components as dcc
from app.pages import index, about, chime, contact, contribute
from app.components.layout import layout
from dash.dependencies import Input, Output


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
    else:
        return dcc.Markdown('## Page not found')

if __name__ == '__main__':
    PENN_CHIME.run_server(debug=True)
