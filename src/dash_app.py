"""Script which launches dash app
"""
from dash import Dash
from chime_dash.layout import setup, EXTERNAL_STYLESHEETS


LANGUAGE = "en"


APP = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
APP.layout = setup(LANGUAGE)


def main():
    """Starts a dash app
    """
    APP.run_server(debug=True)


if __name__ == "__main__":
    main()
