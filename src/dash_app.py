"""Script which launches dash app
"""
from dash import Dash
from dash.dependencies import Input, Output
from dash_core_components import Markdown

import dash_bootstrap_components as dbc

from penn_chime.settings import DEFAULTS
from chime_dash.utils import (
    get_md_templates,
    get_yml_templates,
    render_yml,
)
from chime_dash.presentation import display_sidebar


EXTERNAL_STYLESHEETS = [
    "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
    dbc.themes.BOOTSTRAP,
]
LANGUAGE = "en"
MD_TEMPLATES = get_md_templates()
YML_TEMPLATES = get_yml_templates()


SIDEBAR_HTML, RENDER_KEYS = display_sidebar(LANGUAGE, DEFAULTS)

APP = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
APP.layout = dbc.Row(
    children=[
        dbc.Col(id="sidebar", children=SIDEBAR_HTML, width=4, className="mt-4",),
        dbc.Col(
            children=render_yml(YML_TEMPLATES[LANGUAGE]["header.yml"])
            + [
                Markdown(id="intro"),
                Markdown(MD_TEMPLATES[LANGUAGE]["placeholder.md"]),
                Markdown(MD_TEMPLATES[LANGUAGE]["definitions.md"]),
                Markdown(MD_TEMPLATES[LANGUAGE]["footer.md"]),
            ],
            width=8,
            className="mt-4",
        ),
    ],
    className="container",
)


@APP.callback(
    Output(component_id="intro", component_property="children"),
    [Input(component_id=key, component_property="value") for key in RENDER_KEYS],
)
def render_intro(*args):
    """Renders intro depending on parameter values
    """
    kwargs = {key: val for key, val in zip(RENDER_KEYS, args)}
    # pars = Parameters(**kwargs)
    return MD_TEMPLATES[LANGUAGE]["intro.md"]  # .format(**kwargs)


def main():
    """Starts a dash app
    """
    APP.run_server(debug=True)


if __name__ == "__main__":
    main()
