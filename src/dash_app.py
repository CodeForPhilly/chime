"""Script which launches dash app
"""
from dash import Dash
from flask import Flask

from penn_chime.settings import DEFAULTS

from chime_dash.components import setup, EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS
from chime_dash.components import CALLBACK_INPUTS, CALLBACK_OUTPUTS, callback_body

LANGUAGE = "en"


def main():
    """Starts a dash app
    """
    app = Dash(
        __name__,
        external_stylesheets=EXTERNAL_STYLESHEETS,
        external_scripts=EXTERNAL_SCRIPTS,
    )
    app.layout = setup(LANGUAGE, DEFAULTS)

    @app.callback(CALLBACK_OUTPUTS, CALLBACK_INPUTS)
    def callback(*args):  # pylint: disable=W0612
        return callback_body(*args, language=LANGUAGE, defaults=DEFAULTS)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
