"""Script which launches dash app
"""
from dash import Dash

from penn_chime.settings import DEFAULTS

from chime_dash.app.components import Body

LANGUAGE = "en"


def main():
    """Starts a dash app
    """
    body = Body(LANGUAGE, DEFAULTS)
    app = Dash(
        __name__,
        external_stylesheets=body.external_stylesheets,
        external_scripts=body.external_scripts,
    )
    app.layout = body.html

    @app.callback(body.callback_outputs, body.callback_inputs)
    def callback(*args):  # pylint: disable=W0612
        return body.callback(*args)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
