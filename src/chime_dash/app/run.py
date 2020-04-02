"""app/run

Defines the Dash instance
"""

from dash import Dash
from penn_chime.settings import DEFAULTS
from chime_dash.app.pages.root import Root
from chime_dash.app.utils.callbacks import wrap_callbacks

LANGUAGE = "en"

body = Root(LANGUAGE, DEFAULTS)

DASH = Dash(
    __name__,
    external_stylesheets=body.external_stylesheets,
    external_scripts=body.external_scripts,
)
DASH.title = "Penn Medicine CHIME"  #! Should be moved into config / out of view
DASH.layout = body.html
wrap_callbacks(DASH)

# server = DASH.server
