"""Initializes the  dash html
"""
from collections import OrderedDict

import dash_bootstrap_components as dbc
from chime_dash.app.components.base import Component, HTMLComponentError
from chime_dash.app.components.content import Content
from chime_dash.app.components.sidebar import Sidebar


class Container(Component):
    """
    """

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            sidebar=Sidebar(language, defaults),
            content=Content(language, defaults),
        )

    def get_html(self):
        """Initializes the content container dash html
        """
        container = dbc.Container(
            children=dbc.Row(self.components["sidebar"].html + self.components["content"].html),
            fluid=True,
            className="mt-5",
        )

        return [container]
