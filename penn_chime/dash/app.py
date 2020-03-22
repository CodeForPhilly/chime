from os import path

from dash import Dash
from dash_core_components import Graph, Slider, Markdown
from dash_html_components import H1, Div
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from penn_chime.dash.utils import (
    df_to_html_table,
    get_md_templates,
    get_yml_templates,
    render_yml,
)
from penn_chime.dash.plotting import get_figure_data
from penn_chime.dash.tmp_data import DF

EXTERNAL_STYLESHEETS = [
    "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css"
]
LANGUAGE = "en"
MD_TEMPLATES = get_md_templates()
YML_TEMPLATES = get_yml_templates()

APP = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
APP.layout = Div(
    children=[
        *render_yml(YML_TEMPLATES[LANGUAGE]["header.yml"]),
        Markdown(MD_TEMPLATES[LANGUAGE]["intro.md"]),
        Graph(id="example-graph"),
        Slider(id="y-max", min=0, max=4, value=1, step=0.5),
        df_to_html_table(DF),
        Markdown(MD_TEMPLATES[LANGUAGE]["definitions.md"]),
        Markdown(MD_TEMPLATES[LANGUAGE]["footer.md"]),
    ]
)

APP.callback(Output("example-graph", "figure"), [Input("y-max", "value")])(
    get_figure_data
)


def main():
    """Starts a dash app
    """
    APP.run_server(debug=True)


if __name__ == "__main__":
    main()
