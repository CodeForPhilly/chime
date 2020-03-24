"""Initializes dropdown menu
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
                ),
                dbc.DropdownMenuItem(
                    "Contact Us",
                    href="http://predictivehealthcare.pennmedicine.org/contact/",
                    external_link=True,
                ),
                dbc.DropdownMenuItem(
                    "User Docs",
                    href="https://code-for-philly.gitbook.io/chime/",
                    external_link=True,
                ),
                dbc.DropdownMenuItem(
                    "GitHub",
                    href="https://github.com/CodeForPhilly/chime",
                    external_link=True,
                ),
                dbc.DropdownMenuItem(
                    "Slack",
                    href="https://codeforphilly.org/chat?channel=covid19-chime-penn",
                ),
            ],
            in_navbar=True,
            label="Learn More",
            color="light",
        )
        return [menu]
