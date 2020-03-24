"""Navigation bar view
"""
from typing import List

import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.development.base_component import ComponentMeta

from penn_chime.defaults import Constants
from penn_chime.settings import DEFAULTS

from chime_dash.app.components.base import Component
from chime_dash.app.components.menu import Menu


class Navbar(Component):
    """
    """

    def __init__(self, language: str = "en", defaults: Constants = DEFAULTS):
        """Sets up self, menue and header
        """
        super().__init__(language, defaults=defaults)
        self.menu = Menu(language, defaults=defaults)

    def get_html(self) -> List[ComponentMeta]:
        """Initialize the navigation bar
        """
        nav = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    dbc.NavbarBrand(
                                        children="Penn Medicine CHIME", href="/"
                                    )
                                ),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                        href="https://www.pennmedicine.org/",
                    ),
                ]
                + self.menu.html
            )
        )
        return [nav]
