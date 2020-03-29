"""Script which launches dash app
"""
from dash import Dash
from chime_dash.app.components import root
from chime_dash.app.utils.callbacks import wrap_callbacks

DASH_APP = Dash(
    __name__,
    external_stylesheets=root.external_stylesheets,
    external_scripts=root.external_scripts,
)
DASH_APP.title = 'Penn Medicine CHIME'
DASH_APP.layout = root.html
wrap_callbacks(DASH_APP)

if __name__ == "__main__":
    DASH_APP.run_server(host='0.0.0.0')
