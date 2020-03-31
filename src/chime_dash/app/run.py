"""app/run

Defines the Dash instance
"""

from dash import Dash
from penn_chime.settings import DEFAULTS
from chime_dash.app.components import Body
LANGUAGE = "en"


STYLESHEETS = Body(LANGUAGE, DEFAULTS).external_stylesheets
SCRIPTS     = Body(LANGUAGE, DEFAULTS).external_scripts

DASH = Dash(
    __name__,
    external_stylesheets=STYLESHEETS,
    external_scripts=SCRIPTS,
)

# server = DASH.server
