"""pages/index
Homepage
"""
from typing import List

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.development.base_component import ComponentMeta

from chime_dash.app.components import navbar
from chime_dash.app.static.homepage import introducing_chime, latest_updates


def render (language: str) -> List[ComponentMeta]:
    """Initializes page
    """
    layout = html.Div(
        [
            dbc.Row(navbar.setup(language)),
            dbc.Col(
                children=introducing_chime('en')
            ),
            dbc.Col(
                children=latest_updates('en')
            )
        ]
    )
    return layout
