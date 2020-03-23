"""Script which launches dash app
"""
from dash import Dash

from penn_chime.settings import DEFAULTS

from chime_dash.layout import setup, EXTERNAL_STYLESHEETS
from chime_dash.layout import CALLBACK_INPUTS, CALLBACK_OUTPUTS, callback_body

LANGUAGE = "en"


def main():
    """Starts a dash app
    """
    app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
    app.layout = setup(LANGUAGE, DEFAULTS)
    app.callback(CALLBACK_OUTPUTS, CALLBACK_INPUTS)(callback_body)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
