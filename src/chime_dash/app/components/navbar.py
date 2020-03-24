"""Navigation bar view
"""
from typing import List, Any
from chime_dash.app.components import header
from chime_dash.app.components import menu

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.development.base_component import ComponentMeta


def setup (language: str) -> List[ComponentMeta]:
    """Initialize the navigation bar
    """
    nav = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        children=[
                            dbc.Col(header.setup(language)),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    children='Penn Medicine CHIME',
                                    href='/')
                            )
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href='https://www.pennmedicine.org/'),
                menu.setup()
            ]
        ))
    return nav
