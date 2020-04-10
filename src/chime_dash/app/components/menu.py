"""component/menu
Dropdown menu which appears on the navigation bar at the top of the screen

refactor incoming
"""
from typing import List

from dash.development.base_component import ComponentMeta
import dash_bootstrap_components as dbc

from chime_dash.app.components.base import Component


class Menu(Component):
    """
    """

    def get_html(self) -> List[ComponentMeta]:
        menu = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Penn Medicine", header=True),
                dbc.DropdownMenuItem(
                    "Predictive Healthcare",
                    href="http://predictivehealthcare.pennmedicine.org/",
                    external_link=True,
                    target="_blank",
                ),
                dbc.DropdownMenuItem(
                    "How to Use CHIME",
                    href="https://code-for-philly.gitbook.io/chime/",
                    external_link=True,
                    target="_blank",
                ),
            ],
            in_navbar=True,
            label="Learn More",
            color="light",
            right=True
        )
        return [menu]
