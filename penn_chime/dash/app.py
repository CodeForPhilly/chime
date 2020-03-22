from os import path

from dash import Dash
from dash_core_components import Graph, Slider, Markdown
from dash_html_components import H1, Div
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from penn_chime.dash.utils import df_to_html_table, get_md_templates
from penn_chime.dash.plotting import get_figure_data
from penn_chime.dash.tmp_data import DF

EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
LANGUAGE = "en"

MD_TEMPLATES = get_md_templates()

APP = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
APP.layout = Div(
    children=[
        H1(children="Hello Dash"),
        Div(children="Dash: A web application framework for Python."),
        Graph(id="example-graph"),
        Slider(id="y-max", min=0, max=4, value=1, step=0.5),
        Markdown(MD_TEMPLATES[LANGUAGE]["table-intro.md"]),
        df_to_html_table(DF),
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
