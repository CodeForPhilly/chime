"""components/navbar
Navigation bar view
"""
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html
from chime_dash.app.components.base import Component
from chime_dash.app.components.menu import Menu
from dash.development.base_component import ComponentMeta
from penn_chime.defaults import Constants
from penn_chime.settings import DEFAULTS


class Navbar(Component):
    """Navigation bar contains menu and brand
    TODO refactor / design input on style and layout
    """

    def __init__(self, language: str = "en", defaults: Constants = DEFAULTS):
        """Sets up self, menu and header
        """
        super().__init__(language, defaults=defaults)
        self.menu = Menu(language, defaults=defaults)

    def get_html(self) -> List[ComponentMeta]:
        """Initialize the navigation bar
        """
        nav = dbc.Navbar(
            children=dbc.Container(
                [
                    dbc.Row(
                        children=[
                            html.A(
                                href="https://www.pennmedicine.org",
                                className="penn-medicine-header__logo",
                                title="Go to the Penn Medicine home page",
                            ),
                            dbc.NavbarBrand(
                                children="CHIME", href="/"
                            ),
                        ],
                        align="center",
                        no_gutters=True,
                    ),

                ]
                + self.menu.html
            ),
            dark=True,
            fixed="top",
            color="dark"
        )
        return [nav]
