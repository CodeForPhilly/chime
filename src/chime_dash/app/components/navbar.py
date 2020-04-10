"""components/navbar
Navigation bar view
"""
from typing import List

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.development.base_component import ComponentMeta

from chime_dash.app.components.base import Component
from chime_dash.app.components.menu import Menu

from penn_chime.parameters import Parameters


class Navbar(Component):
    """Navigation bar contains menu and brand
    TODO refactor / design input on style and layout
    """

    def __init__(self, language: str = "en", defaults: Parameters = None):
        """Sets up self, menu and header
        """
        super().__init__(language, defaults=defaults)
        self.menu = Menu(language, defaults=defaults)

    def get_html(self) -> List[ComponentMeta]:
        """Initialize the navigation bar
        """
        nav = dbc.Navbar(
            className="penn-medicine-header px-0",
            children=html.Div(
                className="d-flex align-items-center w-100",
                children=[
                    html.Div(
                        className="px-3",
                        style={"width": "320px"},
                        children=html.A(
                            href="https://www.pennmedicine.org",
                            className="penn-medicine-header__logo",
                            title="Go to the Penn Medicine home page",
                        ),
                    ),
                    html.Div(
                        className="flex-fill",
                        children=dbc.Container(
                            children=[dbc.NavbarBrand(
                                children=html.H1(
                                    style={"font": "inherit", "margin": "0"},
                                    children="COVID-19 Hospital Impact Model for Epidemics (CHIME)"
                                ),
                                href="/"
                            )] + self.menu.html
                        ),
                    )
                ],
            ),
            dark=True,
            fixed="top",
            color="",
        )
        return [nav]
